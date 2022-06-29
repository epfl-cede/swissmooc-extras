import datetime
import logging
import os
import gzip
import gnupg
import pathlib
from dateutil import parser

from django.conf import settings
from django.core.management.base import BaseCommand

from split_logs.models import Organisation, PLATFORM_OLD, PLATFORM_NEW

logger = logging.getLogger(__name__)

MTIME_LESS_DAYS_AGO = 2
MTIME_GREATER_DAYS_AGO = 30

class Command(BaseCommand):
    help = 'Encrypt files with organization keys and put it on SWITCH Drive'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)
        parser.add_argument('--platform', type=str, default=PLATFORM_OLD)

    def handle(self, *args, **options):
        if options['platform'] == PLATFORM_OLD:
            logger.info("get files for split from old platform")
            self._handle_old(options['limit'])
        elif options['platform'] == PLATFORM_NEW:
            logger.info("get files for split from new platform")
            self._handle_new(options['limit'])
        else:
            logger.warning("unknown platform <{}>".format(options['platform']))

    def _handle_old(self, limit):
        self.splitted_dir = settings.TRACKING_LOGS_SPLITTED
        self.encrypted_dir = settings.TRACKING_LOGS_ENCRYPTED

        self._loop_organizations(limit)

    def _handle_new(self, limit):
        self.splitted_dir = settings.TRACKING_LOGS_SPLITTED_DOCKER
        self.encrypted_dir = settings.TRACKING_LOGS_ENCRYPTED_DOCKER

        self._loop_organizations(limit)

    def _loop_organizations(self, limit):
        cnt = 0
        organisations = Organisation.objects.filter(active=True)
        for o in organisations:
            logger.info("process organisation {}".format(o.name))

            files_for_process = self._get_files_for_process(o)

            gpg = gnupg.GPG()
            gpg.encoding = 'utf-8'
            importres = gpg.import_keys(o.public_key.value)
            gpg.trust_keys(importres.fingerprints, 'TRUST_ULTIMATE')

            for file_name, alias_list in files_for_process.items():
                logger.info("process file %s for organization %s with aliases %s", file_name, alias_list[0][0], list(map(lambda a: a[1], alias_list)))

                # collect data into temporary file
                buff = b''
                for org in alias_list:
                    orig_file_full_path = "{}/{}/{}".format(self.splitted_dir, org[1], file_name)
                    with open(orig_file_full_path, 'rb') as f:
                        buff += f.read()

                status = gpg.encrypt(buff,
                                          armor=True,
                                          recipients=[o.public_key.recipient],
                                          output=self._get_encrypted_file_full_path(o, file_name)
                )
                if status.ok:
                    logger.info("success encrypt file %s", self._get_encrypted_file_full_path(o, file_name))
                else:
                    logger.error("error: %s", status.status)

                cnt += 1
                if cnt >= limit: break

    def _get_encrypted_file_full_path(self, organisation, fname):
        return "{}/{}/{}-courseware-events-{}.gpg".format(
            self.encrypted_dir,
            organisation.name,
            organisation.name.lower(),
            fname
        )

    def _get_files_for_process(self, organisation):
        aliases = organisation.aliases.split(',')
        result = {}
        for a in aliases:
            org = a.strip()
            filelist = self._get_list(org)
            for orig_file in filelist:
                orig_file_full_path = "{}/{}/{}".format(self.splitted_dir, org, orig_file)
                less_days_ago = datetime.datetime.now() - datetime.timedelta(days=MTIME_LESS_DAYS_AGO)
                greater_days_ago = datetime.datetime.now() - datetime.timedelta(days=MTIME_GREATER_DAYS_AGO)
                mtime = os.path.getmtime(orig_file_full_path)
                # skip files created less then 2 days ago
                if mtime < less_days_ago.timestamp() and mtime > greater_days_ago.timestamp():
                    pathlib.Path("{}/{}".format(self.encrypted_dir, organisation.name)).mkdir(parents=True, exist_ok=True)
                    if not os.path.isfile(self._get_encrypted_file_full_path(organisation, orig_file)):
                        if orig_file not in result: result[orig_file] = list()
                        result[orig_file].append((organisation.name, org))
        return result

    def _get_list(self, org):
        files = list()
        try:
            path = "{}/{}".format(self.splitted_dir, org)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except FileNotFoundError:
            logger.warning("folder for organisation alias %s does not exist", org)
        return files
