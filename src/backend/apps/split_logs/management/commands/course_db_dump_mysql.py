# -*- coding: utf-8 -*-
import datetime
import logging
import os
import pathlib

from apps.split_logs.models import Course
from apps.split_logs.models import CourseDump
from apps.split_logs.models import CourseDumpTable
from apps.split_logs.models import DB_TYPE_MYSQL
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand


logger = logging.getLogger(__name__)

TABLE_COLUMNS = {}


class Command(SMSCommand):
    help = "Course DB dump tables"

    def handle(self, *args, **options):
        self.setOptions(**options)

        self._fill_mysql_tables_columns()
        organisations = Organisation.objects.filter(
            active=True,
            public_key__isnull=False,
        )
        tables = CourseDumpTable.objects.all()
        for o in organisations:
            logger.info(f"process organisation <{o.name}>")
            for course in o.course_set.filter(active=True):
                for table in tables:
                    if table.db_type == DB_TYPE_MYSQL:
                        # check it we have processed it already
                        processed = CourseDump.objects.filter(
                            course=course,
                            table=table,
                            date=datetime.datetime.now()
                        ).count()
                        if processed == 0:
                            self._process_mysql_table(o, course, table)

    def _process_mysql_table(self, organisation, course, table):
        users = self._get_mysql_users(organisation, course)
        data = self._dump_mysql_table(organisation, course, table, users)
        try:
            cd = CourseDump.objects.get(
                course=course,
                table=table,
                date=datetime.datetime.now()
            )
        except CourseDump.DoesNotExist:
            cd = CourseDump(
                course=course,
                table=table,
                date=datetime.datetime.now()
            )

        dump_file_name = cd.dump_file_name()
        pathlib.Path(os.path.dirname(dump_file_name)).mkdir(
            parents=True,
            exist_ok=True
        )
        logger.info(f"dump <{table.name}> table into <{dump_file_name}>")
        with open(dump_file_name, "w") as f:
            for d in data:
                f.write("{}\n".format("\t".join(map(lambda a: str(a).strip(), d))))
            f.close()

        cd.save()

    def _fill_mysql_tables_columns(self):
        cursor = self.edxapp_cursor()
        for table in CourseDumpTable.objects.all():
            if table.db_type == DB_TYPE_MYSQL:
                sql = "SHOW COLUMNS FROM {table_db_name}.{table_name}".format(
                    table_db_name=table.db_name,
                    table_name=table.name,
                )
                cursor.execute(sql)
                TABLE_COLUMNS[table.id] = [str(row[0]) for row in cursor.fetchall()]

    def _dump_mysql_table(self, organisation, course, table, users):
        if users == [] : users = [0]
        logger.info(f"dump course <{course}> table <{table}>")
        sql = "SELECT `{columns}` FROM {db_name}.{table_name} WHERE {pk} IN(%s)".format(
            db_name="docker_" + organisation.name.lower() + "_edxapp",
            columns="`,`".join(TABLE_COLUMNS[table.id]),
            table_name=table.name,
            pk=table.primary_key
        )
        cursor = self.edxapp_cursor()
        format_strings = ",".join(["%s"] * len(users))
        cursor.execute(sql % format_strings, tuple(users))
        result = [list(row) for row in cursor.fetchall()]

        # remove passwords
        if "password" in TABLE_COLUMNS[table.id]:
            index = TABLE_COLUMNS[table.id].index("password")
            for i in range(len(result)):
                result[i][index] = "NULL"

        # table header
        result.insert(0, TABLE_COLUMNS[table.id])
        return result

    def _get_mysql_users(self, organisation, course):
        cursor = self.edxapp_cursor()
        cursor.execute(
            "SELECT user_id FROM {db_name}.student_courseenrollment WHERE course_id = %s".format(
                db_name="docker_" + organisation.name.lower() + "_edxapp"
            ),
            (course.course_id,)
        )
        return [row[0] for row in cursor.fetchall()]
