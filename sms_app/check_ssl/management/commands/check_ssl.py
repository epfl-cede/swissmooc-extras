import sys
import datetime
import ssl
import socket


from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from check_ssl.models import Site

WARNING_DELTA = datetime.timedelta(days=7)

class Command(BaseCommand):
    help = 'Check SSL expiration dates and set it to the database'

    def handle(self, *args, **options):
        sites = Site.objects.all()
        now = datetime.datetime.now()
        result = 0
        mail_log = {
            'for_update': [],
            'with_error': [],
        }
        for site in sites:
            try:
                expires = self._ssl_expiry_datetime(site.hostname)
            except ssl.CertificateError as e:
                site.error = 'cert error {}'.format(e)
                mail_log['with_error'].append("{}\t{}".format(site.hostname, site.error))
            except ssl.SSLError as e:
                site.error = 'cert error {}'.format(e)
                mail_log['with_error'].append("{}\t{}".format(site.hostname, site.error))
            except socket.timeout as e:
                site.error = 'could not connect'
                mail_log['with_error'].append("{}\t{}".format(site.hostname, site.error))
            except socket.gaierror as e:
                site.error = 'not accessable'
                mail_log['with_error'].append("{}\t{}".format(site.hostname, site.error))
            else:
                site.expires = expires
                site.error = ''
                if expires - now < WARNING_DELTA:
                    self.stdout.write(self.style.ERROR('Site SSL cert will expire at %s, have to update cert' % expires))
                    result = 1
                    mail_log['for_update'].append("{}\t{}".format(site.hostname, site.expires))

            site.save()

        self._send_mail(mail_log)
        sys.exit(result)

    def _send_mail(self, mail_log):
        now = datetime.datetime.now().date()
        send_mail(
            '[SMS-extras:{env}] Check SSL result - {date}'.format(
                env=settings.SMS_APP_ENV,
                date=now
            ),
            '''
Need your attention!

Expired soon hostnames:
{}
With errors hostnames:
{}
            '''.format(
                now,
                '\n'.join(mail_log['for_update']),
                '\n'.join(mail_log['with_error']),
            ),
            settings.EMAIL_FROM_ADDRESS,
            settings.EMAIL_TO_ADDRESSES,
            fail_silently=False,
        )

    def _ssl_expiry_datetime(self, hostname: str) -> datetime.datetime:
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=hostname,
        )
        # 3 second timeout because Lambda has runtime limitations
        conn.settimeout(3.0)

        self.stdout.write(self.style.SUCCESS('Connect to %s' % hostname))
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()
        # parse the string from the certificate into a Python datetime object
        return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
