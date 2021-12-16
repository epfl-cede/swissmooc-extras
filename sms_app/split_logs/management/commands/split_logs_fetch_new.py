import subprocess
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch new tracking logs files'

    def handle(self, *args, **options):
        # copy tracking logs files from old platform
        cmd = [
            "rsync",
            "-av",
            "--exclude=*.log",
            settings.TRACKING_LOGS_ORIGINAL_SRC,
            settings.TRACKING_LOGS_ORIGINAL_DST
        ]
        logger.info("run command: {}".format(" ".join(cmd)))
        subprocess.run(cmd, shell=False, check=True)

        # copy tracking logs files from new docker-based platform
        cmd = [
            "rsync",
            "-e",
            "ssh -i '/home/ubuntu/.ssh/id_rsa_backup'",
            "-av",
            "--exclude=*.log",
            settings.TRACKING_LOGS_ORIGINAL_DOCKER_SRC,
            settings.TRACKING_LOGS_ORIGINAL_DOCKER_DST
        ]
        logger.info("run command: {}".format(" ".join(cmd)))
        subprocess.run(cmd, shell=False, check=True)
