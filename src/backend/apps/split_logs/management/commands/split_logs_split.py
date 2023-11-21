# -*- coding: utf-8 -*-
import gzip
import json
import logging
import os

from apps.split_logs.models import DirOriginal
from apps.split_logs.models import FileOriginal
from apps.split_logs.models import FileOriginalDocker
from apps.split_logs.models import PLATFORM_NEW
from apps.split_logs.models import PLATFORM_OLD
from apps.split_logs.sms_command import SMSCommand
from dateutil import parser
from django.conf import settings
from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Concat

logger = logging.getLogger(__name__)


class Command(SMSCommand):
    help = 'Split tracking logs by organisations'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)
        parser.add_argument('--platform', type=str, default=PLATFORM_OLD)

    def handle(self, *args, **options):
        self.setOptions(**options)

        if options['platform'] == PLATFORM_OLD:
            logger.info("get files for split from old platform")
            self.platform = 'old'
            self._handle_old(options['limit'])
        elif options['platform'] == PLATFORM_NEW:
            logger.info("get files for split from new platform")
            self.platform = 'new'
            self._handle_new(options['limit'])
        else:
            logger.warning(f"unknown platform <{options['platform']}>")

    def _handle_old(self, limit):
        self.original_dir = settings.TRACKING_LOGS_ORIGINAL_DST
        self.splitted_dir = settings.TRACKING_LOGS_SPLITTED
        self.file_model = FileOriginal

        # get list of original files
        originals = self._get_list()

        # get list of processed files
        processed = self._get_processed()

        # loop through files
        self._loop_files(originals, processed, limit)

    def _handle_new(self, limit):
        self.original_dir = settings.TRACKING_LOGS_ORIGINAL_DOCKER_DST
        self.splitted_dir = settings.TRACKING_LOGS_SPLITTED_DOCKER
        self.file_model = FileOriginalDocker

        # get list of original files
        originals = self._get_list()

        # get list of processed files
        processed = self._get_processed()

        # loop through files
        self._loop_files(originals, processed, limit)

    def _loop_files(self, originals, processed, limit):
        cnt = 0
        for dirname, files in originals.items():
            for filename in files:
                filename_full = "{}/{}".format(dirname, filename)
                if filename_full in processed:
                    logger.debug(f"file <{filename_full}> already processed")
                else:
                    # create dir row if not exists
                    dir_original, created = DirOriginal.objects.update_or_create(name=dirname)

                    total, error = self._process_file(dirname, filename)
                    file_original = self.file_model(dir_original=dir_original, name=filename, lines_total=total, lines_error=error)
                    file_original.save()
                    cnt += 1
                    processed.append(filename_full)
                if cnt >= limit: break
            if cnt >= limit: break
        if cnt == 0:
            logger.info("all files were processed before this run")
        else:
            logger.info(f"{cnt} files were processed")

    def _get_processed(self):
        return list(
            self.file_model.objects
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
                    # detect orzanization string
                    organisation = self._detect_org(data['context'], dirname)

                    logger.debug(f"line for organisation <{organisation}>")

                    # create dir
                    splited_dir = '{}/{}'.format(self.splitted_dir, organisation)
                    try:
                        os.mkdir(splited_dir)
                    except FileExistsError:
                        pass

                    # put line to corresponding files
                    if organisation not in lines_for_add:
                        lines_for_add[organisation] = {}
                    if date not in lines_for_add[organisation]:
                        lines_for_add[organisation][date] = []

                    lines_for_add[organisation][date].append(line)

        # bunch adding lines, to prevent posibility for duplicates
        for organisation in lines_for_add:
            for date in lines_for_add[organisation]:
                splited_filename = '{}/{}/{}.log.gz'.format(self.splitted_dir, organisation, date)
                splited_file = gzip.open(splited_filename, 'ab+')
                splited_file.write(b''.join(lines_for_add[organisation][date]))

        logger.info(f"error lines {lines_error} of {lines_total}")
        return lines_total, lines_error

    def _detect_org(self, context, dirname):
        if self.platform == 'old':
            try:
                if context['org_id']:
                    organisation = context['org_id']
                else:
                    organisation = '_empty'
            except KeyError:
                organisation = '_none'
        else:
            organisation = dirname.split('/')[0]

        return organisation

    def _get_list(self):
        dirs = {}
        for (dirpath, dirnames, filenames) in os.walk(self.original_dir):
            files = [fi for fi in filenames if fi.endswith(".gz")]
            if len(files):
                files.sort()
                dirs[dirpath[len(self.original_dir)+1:]] = files
        return dirs
