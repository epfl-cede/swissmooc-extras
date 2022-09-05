# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import pathlib
import subprocess
import tempfile

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import connections
from split_logs.models import ACTIVE
from split_logs.models import Course
from split_logs.models import CourseDump
from split_logs.models import CourseDumpTable
from split_logs.models import DB_TYPE_MONGO
from split_logs.models import DB_TYPE_MYSQL
from split_logs.models import NO
from split_logs.models import NOT_ACTIVE
from split_logs.models import Organisation
from split_logs.models import YES

logger = logging.getLogger(__name__)

TABLE_COLUMNS = {}

class Command(BaseCommand):
    help = 'Course DB dump mongo tables'
    data_files = {}

    def handle(self, *args, **options):
        organisations = Organisation.objects.filter(active=True)
        tables = CourseDumpTable.objects.all()
        for o in organisations:
            logger.info("process organization %s", o.name)
            self._dump_mongo_tabes(o)
            for course in o.course_set.filter(active=ACTIVE):
                for table in tables:
                    if table.db_type == DB_TYPE_MONGO:
                        # check it we have processed it already
                        processed = CourseDump.objects.filter(course=course, table=table, date=datetime.datetime.now()).count()
                        if processed == 0:
                            self._process_mongo_table(course, table)

    def _process_mongo_table(self, course, table):
        try:
            cd = CourseDump.objects.get(course=course, table=table, date=datetime.datetime.now())
        except CourseDump.DoesNotExist:
            cd = CourseDump(course=course, table=table, date=datetime.datetime.now())

        dump_file_name = cd.dump_file_name()
        pathlib.Path(os.path.dirname(dump_file_name)).mkdir(parents=True, exist_ok=True)
        logger.info("dump %s table into %s", table.name, dump_file_name)
        with open(dump_file_name, 'w') as f:
            with open(self.data_files[table.name], 'r') as data:
                for line in data:
                    json_data = json.loads(line)
                    if json_data['course_id'] == course.name:
                        f.write(line)
            f.close()

        cd.save()

    def _dump_mongo_tabes(self, o):
        # dump all data to temporary files
        for table in CourseDumpTable.objects.all():
            if table.db_type == DB_TYPE_MONGO:
                tf = tempfile.NamedTemporaryFile(delete=False)
                cmd = [
                    'mongoexport',
                    '--host', settings.DATABASES['edxapp_readonly']['HOST'],
                    '--username', 'admin',
                    '--password', 'GtTD6ajkaSdzyHH8',
                    '--authenticationDatabase', 'admin',
                    '--db', o.name.lower() + '_' + table.db_name,
                    '--collection', table.name
                ]
                subprocess.run(cmd, shell=False, check=True, stdout=tf)
                tf.close()
                self.data_files[table.name] = tf.name
