import datetime
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Fetch new tracking logs files'

    def handle(self, *args, **options):
        if settings.TRACKING_LOGS_ORIGINAL_SRC and settings.TRACKING_LOGS_ORIGINAL_DST:
            subprocess.call([
                "rsync",
                "-av",
                "--include='*.gz'",
                "--exclude='*'",
                settings.TRACKING_LOGS_ORIGINAL_SRC,
                settings.TRACKING_LOGS_ORIGINAL_DST
            ])
