# -*- coding: utf-8 -*-
import json
import logging
import os
import pathlib
import subprocess
import tempfile
from datetime import date
from datetime import timedelta

from apps.split_logs.models import Course
from apps.split_logs.models import CourseDump
from apps.split_logs.models import CourseDumpTable
from apps.split_logs.models import DB_TYPE_MONGO
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
from django.conf import settings


TABLE_COLUMNS = {}
logger = logging.getLogger(__name__)


class Command(SMSCommand):
    help = "Course DB dump mongo tables"
    data_files = {}
    today = date.today()

    def handle(self, *args, **options):
        self.setOptions(**options)

        organisations = Organisation.objects.filter(
            active=True,
            public_key__isnull=False,
        )
        logger.debug(f"Select <{len(organisations)}> organisations")

        tables = CourseDumpTable.objects.all()
        for o in organisations:
            logger.info(f"process organisation <{o.name}>")
            self._dump_mongo_tabes(o)
            for course in o.course_set.filter(active=True):
                for table in tables:
                    if table.db_type == DB_TYPE_MONGO:
                        # check it we have processed it already
                        processed = CourseDump.objects.filter(
                            course=course,
                            table=table,
                            date=self.today,
                        ).count()
                        if processed == 0:
                            self._process_mongo_table(course, table)

                self._clear_old_records(course, 30)

    def _clear_old_records(self, course: Course, days: int) -> None:
        older = self.today - timedelta(days=days)
        logger.debug(f"Delete records older than {older=}")
        CourseDump.objects.filter(
            course=course,
            date__lt=older,
        ).delete()

    def _process_mongo_table(self, course, table):
        cd, _ = CourseDump.objects.update_or_create(
            course=course,
            table=table,
            date=self.today,
            is_encypted=False,
        )
        logger.info(f"{cd=}")
        dump_file_name = cd.dump_file_name()
        pathlib.Path(os.path.dirname(dump_file_name)).mkdir(
            parents=True,
            exist_ok=True
        )
        logger.info(f"dump {table.name=} table into {dump_file_name=}")
        with open(dump_file_name, "w") as f:
            with open(self.data_files[table.name], "r") as data:
                for line in data:
                    json_data = json.loads(line)
                    if json_data["course_id"] == course.course_id:
                        f.write(line)

        cd.save()

    def _dump_mongo_tabes(self, o):
        # dump all data to temporary files
        for table in CourseDumpTable.objects.all():
            if table.db_type == DB_TYPE_MONGO:
                tf = tempfile.NamedTemporaryFile(delete=False)
                cmd = [
                    "mongoexport",
                    # replace last octet with old backend IP as MongoDb is still there
                    "--host", settings.MONGODB_HOST,
                    "--username", settings.MONGODB_USER,
                    "--password", settings.MONGODB_PASSWORD,
                    "--authenticationDatabase", "admin",
                    "--db", o.name.lower() + "_" + table.db_name,
                    "--collection", table.name
                ]
                subprocess.run(cmd, shell=False, check=True, stdout=tf)
                tf.close()
                self.data_files[table.name] = tf.name
