import logging
import os
from dateutil import parser

from django.conf import settings
from split_logs.utils import upload_file
from django.core.management.base import BaseCommand, CommandError

from split_logs.models import Organisation

logger = logging.getLogger(__name__)

BUCKET = settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS

class Command(BaseCommand):
    help = 'Encrypt files with organization keys and put it on SWITCH Drive'

    def handle(self, *args, **options):
        organisations = Organisation.objects.all()
        for o in organisations:
            aliases = o.aliases.split(',')
            for a in aliases:
                org = a.strip()
                logger.info("process organisation alias '{}'".format(org))
                filelist = self._get_list(org)
                for encripted_file in filelist:
                    upload_file(
                        o,
                        '{}/{}/{}'.format(
                            settings.TRACKING_LOGS_ENCRYPTED,
                            org,
                            encripted_file
                        ),
                        '{}/tracking-logs/{}'.format(org, encripted_file),
                    )

    def _get_list(self, org):
        files = list()
        try:
            path = "{}/{}".format(settings.TRACKING_LOGS_ENCRYPTED, org)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except FileNotFoundError:
            logger.warning("organisation '%s' folder does not exist", org)
        return files
