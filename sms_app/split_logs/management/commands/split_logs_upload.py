import logging
import os
from dateutil import parser

from django.conf import settings
from split_logs.utils import upload_file
from django.core.management.base import BaseCommand, CommandError

from split_logs.models import Organisation, PLATFORM_OLD, PLATFORM_NEW

logger = logging.getLogger(__name__)

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
        self.remote_dir = 'tracking-logs'
        self.encrypted_dir = settings.TRACKING_LOGS_ENCRYPTED

        self._loop_organizations(limit)

    def _handle_new(self, limit):
        self.remote_dir = 'tracking-logs-docker'
        self.encrypted_dir = settings.TRACKING_LOGS_ENCRYPTED_DOCKER

        self._loop_organizations(limit)

    def _loop_organizations(self, limit):
        cnt = 0

        organisations = Organisation.objects.filter(active=True)
        for o in organisations:
            # overwrite BUCKET for docker-based logs
            aliases = o.aliases.split(',')
            for a in aliases:
                org = a.strip()
                logger.info("process organisation alias '{}'".format(org))
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
            return '{}-{}'.format(settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS, str(organisation).lower())
        else:
            return settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS

    def _get_list(self, org):
        files = list()
        try:
            path = "{}/{}".format(self.encrypted_dir, org)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except FileNotFoundError:
            logger.warning("organisation '%s' folder does not exist", org)
        return files
