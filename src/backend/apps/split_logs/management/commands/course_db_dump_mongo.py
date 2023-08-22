# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import pathlib
import re
import subprocess
import tempfile

from apps.split_logs.models import ACTIVE
from apps.split_logs.models import Course
from apps.split_logs.models import CourseDump
from apps.split_logs.models import CourseDumpTable
from apps.split_logs.models import DB_TYPE_MONGO
from apps.split_logs.models import DB_TYPE_MYSQL
from apps.split_logs.models import NO
from apps.split_logs.models import NOT_ACTIVE
from apps.split_logs.models import Organisation
from apps.split_logs.models import YES
from apps.split_logs.sms_command import SMSCommand
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections


TABLE_COLUMNS = {}

class Command(SMSCommand):
    help = "Course DB dump mongo tables"
    data_files = {}
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.handle_verbosity(options)

        organisations = Organisation.objects.filter(active=True)
        self.debug(f"Select <{len(organisations)}> organisations")

        tables = CourseDumpTable.objects.all()
        for o in organisations:
            self.info(f"process organization <{o.name}>")
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
        self.info(f"dump <{table.name}> table into <{dump_file_name}>")
        with open(dump_file_name, "w") as f:
            with open(self.data_files[table.name], "r") as data:
                for line in data:
                    json_data = json.loads(line)
                    if json_data["course_id"] == course.name:
                        f.write(line)
            f.close()

        cd.save()

    def _dump_mongo_tabes(self, o):
        # dump all data to temporary files
        for table in CourseDumpTable.objects.all():
            if table.db_type == DB_TYPE_MONGO:
                tf = tempfile.NamedTemporaryFile(delete=False)
                cmd = [
                    "mongoexport",
                    # replace last octet with old backend IP as MongoDb is still there
                    "--host", re.sub(
                        r'\b(\d+\.\d+\.\d+)\.\d+\b', r'\1.0',
                        settings.EDXAPP_DATABASES["readonly"]["host"]
                    ),
                    "--username", "admin",
                    "--password", "GtTD6ajkaSdzyHH8",
                    "--authenticationDatabase", "admin",
                    "--db", o.name.lower() + "_" + table.db_name,
                    "--collection", table.name
                ]
                subprocess.run(cmd, shell=False, check=True, stdout=tf)
                tf.close()
                self.data_files[table.name] = tf.name
