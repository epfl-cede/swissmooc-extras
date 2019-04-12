import datetime
import ssl
import socket


from django.core.management.base import BaseCommand, CommandError

from check_ssl.models import Site

class Command(BaseCommand):
    help = 'Check SSL expiration dates and set it to the database'

    def handle(self, *args, **options):
        sites = Site.objects.all()
        for site in sites:
            try:
                expires = self._ssl_expiry_datetime(site.hostname)
            except ssl.CertificateError as e:
                site.error = 'cert error {}'.format(e)
            except ssl.SSLError as e:
                site.error = 'cert error {}'.format(e)
            except socket.timeout as e:
                site.error = 'could not connect'
            else:
                site.expires = expires
                site.error = ''
            site.save()

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
