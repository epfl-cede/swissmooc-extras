# -*- coding: utf-8 -*-
import logging

from apps.split_logs.sms_command import SMSCommand
from apps.split_logs.utils import run_command
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(SMSCommand):
    help = 'Fetch new tracking logs files'

    def handle(self, *args, **options):
        self.setOptions(**options)

        logger.info(f"sync files from {settings.BACKUP_SERVER}")
        return_code, stdout, stderr = run_command([
            "rsync",
            "-av",
            "--exclude=*.log",
            f"ubuntu@{settings.BACKUP_SERVER}:{settings.TRACKING_LOGS_ORIGINAL_DOCKER_SRC}",
            settings.TRACKING_LOGS_ORIGINAL_DOCKER_DST
        ])
        if return_code != 0:
            logger.error(f"rsync error: <{stderr}>")
