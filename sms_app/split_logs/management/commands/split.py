import datetime
import subprocess
import logging
import gzip
import json
import os

from os import walk
from dateutil import parser

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from split_logs.models import DirOriginal, FileOriginal

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Split tracking logs by organizations'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)

    def handle(self, *args, **options):
        limit = options['limit']
        cnt = 0

        # list gz files
        originals = self._get_list()
        for dirname, files in originals.items():
            for filename in files:
                # create dir row if not exists
                dir_original, created = DirOriginal.objects.update_or_create(name=dirname)

                # skip already splitted files
                if FileOriginal.objects.filter(dir_original=dir_original, name=filename).count():
                    logger.debug("debug: file already processed")
                else:
                    total, error = self._process_file(dirname, filename)
                    file_original = FileOriginal(dir_original=dir_original, name=filename, lines_total=total, lines_error=error)
                    file_original.save()
                    cnt += 1
                if cnt >= limit: break
            if cnt >= limit: break

    def _process_file(self, dirname, filename):
        logger.debug("debug: process file {}/{}".format(dirname, filename))

        logger.info("info: start split file {}/{}".format(dirname, filename))

        # reset counters
        lines_total = 0
        lines_error = 0

        # read file line by line
        with gzip.open('{}/{}/{}'.format(settings.TRACKING_LOGS_ORIGINAL_DST, dirname, filename), 'rb') as f:
            lines_for_add = {}
            for line in f:
                lines_total += 1
                try:
                    data = json.loads(line.decode('utf-8'))
                except json.decoder.JSONDecodeError as e:
                    lines_error += 1
                except UnicodeDecodeError as e:
                    lines_error += 1
                else:
                    # detect orzanization string
                    time = parser.parse(data['time'])
                    date = time.strftime('%Y-%m-%d')
                    try:
                        if data['context']['org_id']:
                            organization = data['context']['org_id']
                        else:
                            organization = '_empty'
                    except KeyError:
                        organization = '_none'

                    #logger.debug("debug: line for organization %s", organization)
                    #logger.debug("debug: line '%s'", data)

                    # create dir
                    splited_dir = '{}/{}'.format(settings.TRACKING_LOGS_SPLITTED, organization)
                    try:
                        os.mkdir(splited_dir)
                    except FileExistsError as e:
                        pass
                        
                    # put line to corresponding files
                    if organization not in lines_for_add:
                        lines_for_add[organization] = {}
                    if date not in lines_for_add[organization]:
                        lines_for_add[organization][date] = []

                    lines_for_add[organization][date].append(line)

        # bunch adding lines, to prevent posibility for duplicates
        for organization in lines_for_add:
            for date in lines_for_add[organization]:
                splited_filename = '{}/{}/{}.log.gz'.format(settings.TRACKING_LOGS_SPLITTED, organization, date)
                splited_file = gzip.open(splited_filename, 'ab+')
                splited_file.write(b''.join(lines_for_add[organization][date]))

        logger.info("info: error lines {} of {}".format(lines_error, lines_total))
        return lines_total, lines_error
        
        
    def _get_list(self):
        dirs = {}
        for (dirpath, dirnames, filenames) in walk(settings.TRACKING_LOGS_ORIGINAL_DST):
            files = [ fi for fi in filenames if fi.endswith(".gz") ]
            if len(files):
                files.sort()
                dirs[dirpath[len(settings.TRACKING_LOGS_ORIGINAL_DST)+1:]] = files
        return dirs
