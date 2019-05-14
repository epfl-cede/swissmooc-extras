import os
import json
import pathlib
import datetime
import logging
import subprocess
import tempfile

from django.conf import settings
from django.db import connections
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from split_logs.models import Course, CourseDump, CourseDumpTable, Organisation
from split_logs.models import ACTIVE, NOT_ACTIVE, YES, NO, DB_TYPE_MYSQL, DB_TYPE_MONGO

logger = logging.getLogger(__name__)

TABLE_COLUMNS = {}

class Command(BaseCommand):
    help = 'Course DB dump mongo tables'
    data_files = {}

    def handle(self, *args, **options):
        self._dump_mongo_tabes()
        organisations = Organisation.objects.all()
        tables = CourseDumpTable.objects.all()
        for o in organisations:
            logger.info("process organization %s", o.name)
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
        
    def _dump_mongo_tabes(self):
        # dump all data to temporary files
        for table in CourseDumpTable.objects.all():
            if table.db_type == DB_TYPE_MONGO:
                tf = tempfile.NamedTemporaryFile(delete=False)
                cmd = [
                    'mongoexport',
                    '--host', settings.EDXAPP_MYSQL_HOST,
                    '--username', 'admin',
                    '--password', 'GtTD6ajkaSdzyHH8',
                    '--authenticationDatabase', 'admin',
                    '--db', table.db_name,
                    '--collection', table.name
                ]
                subprocess.run(cmd, shell=False, check=True, stdout=tf)
                tf.close()
                self.data_files[table.name] = tf.name
