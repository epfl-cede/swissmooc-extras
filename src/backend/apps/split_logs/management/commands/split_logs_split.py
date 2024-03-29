# -*- coding: utf-8 -*-
import gzip
import json
import logging
import os

from apps.split_logs.models import DirOriginal
from apps.split_logs.models import FileOriginal
from apps.split_logs.models import FileOriginalDocker
from apps.split_logs.sms_command import SMSCommand
from dateutil import parser
from django.conf import settings
from django.db.models import Value
from django.db.models.functions import Concat

logger = logging.getLogger(__name__)


class Command(SMSCommand):
    help = 'Split tracking logs for organisation by date'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)
        parser.add_argument('--org', type=str, default="epfl")

    def handle(self, *args, **options):
        self.setOptions(**options)
        self.limit = options['limit']
        self.org = options['org']

        self.original_dir = f"{settings.TRACKING_LOGS_ORIGINAL_DOCKER_DST}/{self.org}"
        self.splitted_dir = f"{settings.TRACKING_LOGS_SPLITTED_DOCKER}/{self.org}"

        # get list of original files
        originals = self._get_list()
        logger.debug(f"Number of original files {len(originals)=}")

        # get list of processed files
        processed = self._get_processed()
        logger.debug(f"Number of processed files {len(processed)=}")

        # loop through files
        self._loop_files(originals, processed)

    def _loop_files(self, originals, processed):
        cnt = 0
        for dirname, files in originals.items():
            for filename in files:
                filename_full = "{}/{}/{}".format(self.org, dirname, filename)
                if filename_full not in processed:
                    # create dir if not exists
                    dir_original, created = DirOriginal.objects.update_or_create(
                        name=f"{self.org}/{dirname}"
                    )

                    total, error = self._process_file(dirname, filename)
                    FileOriginalDocker.objects.create(
                        dir_original=dir_original,
                        name=filename,
                        lines_total=total,
                        lines_error=error
                    )
                    cnt += 1
                    processed.append(filename_full)
                if cnt >= self.limit: break
            if cnt >= self.limit: break
        if cnt == 0:
            logger.info("all files were processed before this run")
        else:
            logger.info(f"{cnt} files were processed")

    def _get_processed(self):
        return list(
            FileOriginalDocker.objects
                .filter(dir_original__name__startswith=f"{self.org}/")
                .annotate(_name=Concat('dir_original__name', Value('/'), 'name'))
                .values_list('_name', flat=True)
                .order_by('_name')
        )

    def _process_file(self, dirname, filename):
        logger.info(f"process file {dirname}/{filename}")

        # reset counters
        lines_total = 0
        lines_error = 0

        # read file line by line
        with gzip.open('{}/{}/{}'.format(self.original_dir, dirname, filename), 'rb') as f:
            lines_for_add = {}
            for line in f:
                lines_total += 1
                try:
                    data = json.loads(line.decode('utf-8'))
                except json.decoder.JSONDecodeError:
                    lines_error += 1
                except UnicodeDecodeError:
                    lines_error += 1
                else:
                    time = parser.parse(data['time'])
                    date = time.strftime('%Y-%m-%d')

                    try:
                        os.mkdir(self.splitted_dir)
                    except FileExistsError:
                        pass

                    if date not in lines_for_add:
                        lines_for_add[date] = []

                    lines_for_add[date].append(line)

        # bunch adding lines, to prevent posibility for duplicates
        for date in lines_for_add:
            fname = f"{self.splitted_dir}/{date}.log.gz"
            logger.debug(f"Append new lines to file {fname}")
            splited_file = gzip.open(fname, 'ab+',)
            splited_file.write(b''.join(lines_for_add[date]))
            splited_file.close()

        return lines_total, lines_error

    def _get_list(self):
        dirs = {}
        for (dirpath, dirnames, filenames) in os.walk(self.original_dir):
            files = [fi for fi in filenames if fi.endswith(".gz")]
            if len(files):
                files.sort()
                dirs[dirpath[len(self.original_dir)+1:]] = files
        return dirs
