import datetime
import subprocess
import logging
from os import walk

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from split_logs.models import DirOriginal, FileOriginal

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Split tracking logs by organizations'

    def handle(self, *args, **options):
        # list gz files
        originals = self._get_list()
        for dirname, files in originals.items():
            for filename in files:
                self._process_file(dirname, filename)
                #break
            #break

    def _process_file(self, dirname, filename):
        logger.debug("debug: process file {}/{}".format(dirname, filename))

        # create dir if not exists
        dir_original, created = DirOriginal.objects.update_or_create(name=dirname)

        # skip already splitted files
        if FileOriginal.objects.filter(dir_original=dir_original, name=filename).count():
            logger.debug("debug: file already processed")
            return True
        else:
            logger.info("info: start split file {}/{}".format(dirname, filename))
            # read file line by line
            # detect orzanization string
            # put lines to corresponding files
            # create FileOriginal row
            return True
        
        
    def _get_list(self):
        dirs = {}
        for (dirpath, dirnames, filenames) in walk(settings.TRACKING_LOGS_ORIGINAL_DST):
            files = [ fi for fi in filenames if fi.endswith(".gz") ]
            if len(files):
                files.sort()
                dirs[dirpath[len(settings.TRACKING_LOGS_ORIGINAL_DST)+1:]] = files
        return dirs
