# -*- coding: utf-8 -*-
import datetime
import logging
import os
import pathlib

import gnupg
from apps.split_logs.models import Organisation
from apps.split_logs.models import PLATFORM_NEW
from apps.split_logs.models import PLATFORM_OLD
from apps.split_logs.sms_command import SMSCommand
from django.conf import settings

logger = logging.getLogger(__name__)

MTIME_LESS_DAYS_AGO = 2
MTIME_GREATER_DAYS_AGO = 30


class Command(SMSCommand):
    help = 'Encrypt files with organization keys and put it on SWITCH Drive'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)
        parser.add_argument('--platform', type=str, default=PLATFORM_OLD)

    def handle(self, *args, **options):
        self.setOptions(**options)

        if options['platform'] == PLATFORM_OLD:
            logger.info("get files for split from old platform")
            self._handle_old(options['limit'])
        elif options['platform'] == PLATFORM_NEW:
            logger.info("get files for split from new platform")
            self._handle_new(options['limit'])
        else:
            logger.warning(f"unknown platform <{options['platform']}>")

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
        organisations = Organisation.objects.filter(
            active=True,
            public_key__isnull=False,
        )
        for o in organisations:
            logger.info(f"process organisation {o.name}")

            files_for_process = self._get_files_for_process(o)

            gpg = gnupg.GPG()
            gpg.encoding = 'utf-8'
            gpg.import_keys(o.public_key.value)

            for file_name, alias_list in files_for_process.items():
                org = alias_list[0][0]
                aliases = list(map(lambda a: a[1], alias_list))
                logger.debug(
                    f"process {file_name=} for {org=} with {aliases=}"
                )

                # collect data into temporary file
                buff = b''
                for org in alias_list:
                    orig_file_full_path = f"{self.splitted_dir}/{org[1]}/{file_name}"
                    with open(orig_file_full_path, 'rb') as f:
                        buff += f.read()

                status = gpg.encrypt(
                    buff,
                    armor=True,
                    recipients=[o.public_key.recipient],
                    output=self._get_encrypted_file_full_path(o, file_name)
                )
                if status.ok:
                    file_path = self._get_encrypted_file_full_path(o, file_name)
                    logger.info(f"success encrypt {file_path=}")
                else:
                    logger.error(f"error: {status.status}")

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
            logger.warning(f"folder for organisation alias <{org}> does not exist")
        return files
