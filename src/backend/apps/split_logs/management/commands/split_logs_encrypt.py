# -*- coding: utf-8 -*-
import datetime
import logging
import os
import pathlib

import gnupg
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
from apps.split_logs.utils import s3_upload_file
from apps.split_logs.utils import SplitLogsUtilsUploadFileException
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

MTIME_LESS_DAYS_AGO = 2
MTIME_GREATER_DAYS_AGO = 30


class Command(SMSCommand):
    help = 'Encrypt files with organisation keys and put it on SWITCH Drive'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)
        parser.add_argument('--org', type=str, default="epfl")

    def handle(self, *args, **options):
        self.setOptions(**options)
        self.limit = options['limit']
        self.org = options['org']
        self.remote_dir = 'tracking-logs-docker'
        self.splitted_dir = f"{settings.TRACKING_LOGS_SPLITTED_DOCKER}/{self.org}"
        self.encrypted_dir = f"{settings.TRACKING_LOGS_ENCRYPTED_DOCKER}/{self.org.upper()}"

        try:
            self.organisation = Organisation.objects.get(
                name__iexact=self.org,
                active=True,
                public_key__isnull=False,
            )
            self._process()
        except ObjectDoesNotExist:
            logger.error(f"Organization {self.org=} does not exists")

    def _process(self):
        logger.info(f"process {self.organisation.name=}")
        splitted = self._get_list()

        gpg = gnupg.GPG()
        gpg.encoding = 'utf-8'
        gpg.import_keys(self.organisation.public_key.value)

        cnt = 0
        for fname in splitted:
            # collect data into temporary file
            splitted_full_path = f"{self.splitted_dir}/{fname}"
            logger.info(f"Process file {splitted_full_path=}")

            buff = b''
            with open(splitted_full_path, 'rb') as f:
                buff += f.read()

            encrypted_file = self._get_encrypted_file_path(fname)
            status = gpg.encrypt(
                buff,
                armor=True,
                recipients=[self.organisation.public_key.recipient],
                output=encrypted_file
            )
            if status.ok:
                logger.info(f"Encrypt file ok {encrypted_file=}")
            else:
                logger.error(f"Encrypt file error: {status.status=}")

            try:
                self._upload_file(encrypted_file, fname)
                logger.info(f"Upload file ok {encrypted_file=}")
                # os.remove(splitted_full_path)
            except SplitLogsUtilsUploadFileException as err:
                logger.error(f"Upload file error {encrypted_file=} {err=}")

            cnt += 1
            if cnt >= self.limit:
                break

    def _get_encrypted_file_path(self, fname):
        return f"{self.encrypted_dir}/{self._get_encrypted_file_name(fname)}"

    def _get_encrypted_file_name(self, fname):
        return f"{self.organisation.name.lower()}-courseware-events-{fname}.gpg"

    def _get_list(self):
        return [
            f for f in os.listdir(self.splitted_dir) if os.path.isfile(os.path.join(self.splitted_dir, f))
        ]

    def _upload_file(self, encrypted_file, fname):
        remote_fname = f"{self.organisation.name}/{self.remote_dir}/{self._get_encrypted_file_name(fname)}"
        s3_upload_file(
            self.organisation.bucket_name,
            self.organisation,
            encrypted_file,
            remote_fname,
        )
