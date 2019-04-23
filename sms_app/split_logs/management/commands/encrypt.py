import datetime
import subprocess
import logging
import os
import gnupg
from shutil import copyfile
from dateutil import parser

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from split_logs.models import DirOriginal, FileOriginal, Organisation

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
            print(importres)
            for a in aliases:
                org = a.strip()
                logger.debug("process organisation alias '{}'".format(org))
                filelist = self._get_list(org)
                for orig_file in filelist:
                    orig_file_full_path = "{}/{}/{}".format(settings.TRACKING_LOGS_SPLITTED, org, orig_file)
                    two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
                    # skipp files created less then 2 days ago
                    if os.path.getmtime(orig_file_full_path) < two_days_ago.timestamp():
                        encrypted_file_full_path = "{}/{}/{}".format(settings.TRACKING_LOGS_ENCRYPTED, org, orig_file)
                        if not os.path.isfile("{}.gpg".format(encrypted_file_full_path)):
                            status = gpg.encrypt_file(
                                encrypted_file_full_path,
                                recipients=[o.public_key.recipient],
                                output="{}.gpg".format(encrypted_file_full_path)
                            )
                            print(status)
                            break
                    
                
    def _get_list(self, org):
        files = list()
        try:
            path = "{}/{}".format(settings.TRACKING_LOGS_SPLITTED, org)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except FileNotFoundError:
            logger.warning("organisation '%s' folder does not exist", org)
            pass
        return files
            
