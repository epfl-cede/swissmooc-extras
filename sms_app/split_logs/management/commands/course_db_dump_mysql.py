import os
import datetime
import logging
import pathlib
import subprocess
import tempfile

from django.conf import settings
from django.db import connections
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from split_logs.models import Course, CourseDump, CourseDumpTable, Organisation
from split_logs.models import ACTIVE, NOT_ACTIVE, YES, NO, DB_TYPE_MYSQL

logger = logging.getLogger(__name__)

TABLE_COLUMNS = {}

class Command(BaseCommand):
    help = 'Course DB dump tables'

    def handle(self, *args, **options):
        self._fill_mysql_tables_columns()
        organisations = Organisation.objects.all()
        tables = CourseDumpTable.objects.all()
        for o in organisations:
            logger.info("process organization %s", o.name)
            for course in o.course_set.filter(active=ACTIVE):
                for table in tables:
                    if table.db_type == DB_TYPE_MYSQL:
                        # check it we have processed it already
                        processed = CourseDump.objects.filter(course=course, table=table, date=datetime.datetime.now()).count()
                        if processed == 0:
                            self._process_mysql_table(course, table)

    def _process_mysql_table(self, course, table):
        users = self._get_mysql_users(course)
        data = self._dump_mysql_table(course, table, users)
        try:
            cd = CourseDump.objects.get(course=course, table=table, date=datetime.datetime.now())
        except CourseDump.DoesNotExist:
            cd = CourseDump(course=course, table=table, date=datetime.datetime.now())

        dump_file_name = cd.dump_file_name()
        pathlib.Path(os.path.dirname(dump_file_name)).mkdir(parents=True, exist_ok=True)
        logger.info("dump %s table into %s", table.name, dump_file_name)
        with open(dump_file_name, 'w') as f:
            for d in data:
                f.write("{}\n".format("\t".join(map(lambda a: str(a).strip(), d))))
            f.close()

        cd.save()
        
    def _fill_mysql_tables_columns(self):
        with connections['edxapp_readonly'].cursor() as cursor:
            for table in CourseDumpTable.objects.all():
                if table.db_type == DB_TYPE_MYSQL:
                    sql = "SHOW COLUMNS FROM {table_db_name}.{table_name}".format(
                        table_db_name=table.db_name,
                        table_name=table.name,
                    )
                    cursor.execute(sql)
                    TABLE_COLUMNS[table.id] = [str(row[0]) for row in cursor.fetchall()]

    def _dump_mysql_table(self, course, table, users):
        logger.info("dump course %s table %s", course, table)
        with connections['edxapp_readonly'].cursor() as cursor:
            format_strings = ','.join(['%s'] * len(users))
            sql = "SELECT `{columns}` FROM edxapp.{table_name} WHERE {pk} IN(%s)".format(
                columns="`,`".join(TABLE_COLUMNS[table.id]),
                table_name=table.name,
                pk=table.primary_key
            )
            cursor.execute(sql % format_strings, tuple(users))
            result = [list(row) for row in cursor.fetchall()]

            # remove passwords
            if 'password' in TABLE_COLUMNS[table.id]:
                index = TABLE_COLUMNS[table.id].index('password')
                for i in range(len(result)):
                    result[i][index] = 'NULL'

            # table header
            result.insert(0, TABLE_COLUMNS[table.id])
            return result
        
    def _get_mysql_users(self, course):
        with connections['edxapp_readonly'].cursor() as cursor:
            cursor.execute("SELECT user_id FROM edxapp.student_courseenrollment WHERE course_id = %s", [course.name])
            return [row[0] for row in cursor.fetchall()]
