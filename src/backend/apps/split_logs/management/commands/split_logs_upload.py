# -*- coding: utf-8 -*-
import logging
import os

from apps.split_logs.models import Organisation
from apps.split_logs.models import PLATFORM_NEW
from apps.split_logs.models import PLATFORM_OLD
from apps.split_logs.sms_command import SMSCommand
from apps.split_logs.utils import bucket_name
from apps.split_logs.utils import upload_file
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(SMSCommand):
    help = 'Upload files to SWITCH Drive'

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
        self.remote_dir = 'tracking-logs'
        self.encrypted_dir = settings.TRACKING_LOGS_ENCRYPTED

        self._loop_organizations(limit)

    def _handle_new(self, limit):
        self.remote_dir = 'tracking-logs-docker'
        self.encrypted_dir = settings.TRACKING_LOGS_ENCRYPTED_DOCKER

        self._loop_organizations(limit)

    def _loop_organizations(self, limit):
        cnt = 0

        organisations = Organisation.objects.filter(
            active=True,
            public_key__isnull=False,
        )
        for o in organisations:
            # overwrite BUCKET for docker-based logs
            aliases = o.aliases.split(',')
            for a in aliases:
                org = a.strip()
                logger.info(f"process organisation alias <{org}>")
                filelist = self._get_list(org)
                for encripted_file in filelist:
                    upload_file(
                        self._bucket(o),
                        o,
                        '{}/{}/{}'.format(
                            self.encrypted_dir,
                            org,
                            encripted_file
                        ),
                        '{}/{}/{}'.format(org, self.remote_dir, encripted_file),
                    )
                    cnt += 1
                    if cnt >= limit: break

    def _bucket(self, organisation):
        if self.encrypted_dir == settings.TRACKING_LOGS_ENCRYPTED_DOCKER:
            return bucket_name(organisation)
        else:
            return settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS

    def _get_list(self, org):
        files = list()
        try:
            path = "{}/{}".format(self.encrypted_dir, org)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except FileNotFoundError:
            logger.warning(f"folder for organisation <{org}> does not exist")
        return files
