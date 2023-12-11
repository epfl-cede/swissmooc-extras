# -*- coding: utf-8 -*-
import datetime
import logging
import socket
import ssl
import sys

from apps.check_ssl.models import Site
from apps.split_logs.sms_command import SMSCommand
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

WARNING_DELTA = datetime.timedelta(days=7)


class Command(SMSCommand):
    help = "Check SSL expiration dates and set it to the database"

    def handle(self, *args, **options):
        self.setOptions(**options)

        time = datetime.datetime.now()
        sites = Site.objects.all()
        self._info(f"Get {len(sites)} for check")

        for site in sites:
            try:
                expires = self._ssl_expiry_datetime(site.hostname)
            except ssl.CertificateError as e:
                site.error = "cert error {}".format(e)
                self._error(f"{site.hostname}: {site.error}")
            except ssl.SSLError as e:
                site.error = "cert error {}".format(e)
                self._error(f"{site.hostname}: {site.error}")
            except socket.timeout:
                site.error = "could not connect"
                self._error(f"{site.hostname}: {site.error}")
            except socket.gaierror:
                site.error = "not accessable"
                self._error(f"{site.hostname}: {site.error}")
            else:
                site.expires = expires
                site.error = ""
                if expires - time < WARNING_DELTA:
                    self._warning(f"{site.hostname} cert will expire at {expires}, have to update cert")

            site.save()

        if self.is_error or self.is_warning:
            self.send_email("Check SSL")

        sys.exit(1 if self.is_error else 0)

    def _ssl_expiry_datetime(self, hostname: str) -> datetime.datetime:
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=hostname,
        )
        # 3 second timeout because Lambda has runtime limitations
        conn.settimeout(3.0)

        self._info(f"Connect to {hostname}")
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()

        # parse the string from the certificate into a Python datetime object
        return datetime.datetime.strptime(ssl_info["notAfter"], r'%b %d %H:%M:%S %Y %Z')
