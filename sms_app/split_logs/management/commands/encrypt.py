import datetime
import logging
import os
import gzip
import gnupg
import pathlib
from dateutil import parser

from django.conf import settings
from django.core.management.base import BaseCommand

from split_logs.models import Organisation

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Encrypt files with organization keys and put it on SWITCH Drive'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)

    def handle(self, *args, **options):
        limit = options['limit']
        cnt = 0
        organisations = Organisation.objects.all()
        for o in organisations:
            aliases = o.aliases.split(',')
            gpg = gnupg.GPG()
            gpg.encoding = 'utf-8'
            importres = gpg.import_keys(o.public_key.value)
            gpg.trust_keys(importres.fingerprints, 'TRUST_ULTIMATE')
            for a in aliases:
                org = a.strip()
                logger.info("process organisation alias '{}'".format(org))
                filelist = self._get_list(org)
                for orig_file in filelist:
                    orig_file_full_path = "{}/{}/{}".format(settings.TRACKING_LOGS_SPLITTED, org, orig_file)
                    two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
                    # skipp files created less then 2 days ago
                    if os.path.getmtime(orig_file_full_path) < two_days_ago.timestamp():
                        _fname, _fextension = os.path.splitext(orig_file)
                        encrypted_file_full_path = "{}/{}/{}.gpg".format(settings.TRACKING_LOGS_ENCRYPTED, org, _fname)
                        pathlib.Path("{}/{}".format(settings.TRACKING_LOGS_ENCRYPTED, org)).mkdir(parents=True, exist_ok=True)
                        if not os.path.isfile(encrypted_file_full_path):
                            with gzip.open(orig_file_full_path, 'rb') as f:
                                cnt += 1
                                status = gpg.encrypt_file(f,
                                    armor=False,
                                    recipients=[o.public_key.recipient],
                                    output=encrypted_file_full_path
                                )
                                if status.ok:
                                    logger.info("success encrypt file %s", encrypted_file_full_path)
                                else:
                                    logger.error("error: %s", status.status)
                                if cnt >= limit: break
                if cnt >= limit: break
            if cnt >= limit: break

    def _get_list(self, org):
        files = list()
        try:
            path = "{}/{}".format(settings.TRACKING_LOGS_SPLITTED, org)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except FileNotFoundError:
            logger.warning("organisation '%s' folder does not exist", org)
        return files

