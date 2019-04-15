import datetime
import subprocess
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch new tracking logs files'

    def handle(self, *args, **options):
        if settings.TRACKING_LOGS_ORIGINAL_SRC and settings.TRACKING_LOGS_ORIGINAL_DST:
            cmd = [
                "rsync",
                "-av",
                "--exclude=*.log",
                settings.TRACKING_LOGS_ORIGINAL_SRC,
                settings.TRACKING_LOGS_ORIGINAL_DST
            ]
            logger.info("run command: {}".format(" ".join(cmd)))
            subprocess.call(cmd, shell=False, check=True)
