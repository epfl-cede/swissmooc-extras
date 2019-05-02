import os
import datetime
import logging
import pathlib

from django.conf import settings
from django.db import connections
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from split_logs.models import Course, CourseDump, Organisation
from split_logs.models import ACTIVE, NOT_ACTIVE, YES, NO

logger = logging.getLogger(__name__)

TABLES = (
    dict(
        name = 'auth_user',
        pk = 'id',
    ),
    dict(
        name = 'auth_userprofile',
        pk='user_id',
    ),
    dict(
        name = 'certificates_generatedcertificate',
        pk='user_id',
    ),
    dict(
        name = 'student_courseenrollment',
        pk='user_id',
    ),
)
class Command(BaseCommand):
    help = 'Dump course tables'

    def handle(self, *args, **options):
        self._fill_tables_columns()
        organisations = Organisation.objects.all()
        for o in organisations:
            logger.info("process organization %s", o.name)
            for course in o.course_set.filter(active=ACTIVE):
                # check it we have processed it already
                processed = CourseDump.objects.filter(course=course, date=datetime.datetime.now(), is_dumped=YES).count()
                if processed == 0:
                    users = self._get_users(course)
                    for table in TABLES:
                        data = self._dump_table(course, table, users)
                        try:
                            cd = CourseDump.objects.get(course=course, date=datetime.datetime.now())
                        except CourseDump.DoesNotExist:
                            cd = CourseDump(course=course, date=datetime.datetime.now())

                        dump_file_name = cd.dump_file_name(table['name'])
                        pathlib.Path(os.path.dirname(dump_file_name)).mkdir(parents=True, exist_ok=True)
                        logger.info("dump %s table into %s", table['name'], dump_file_name)
                        with open(dump_file_name, 'w') as f:
                            for d in data:
                                f.write("{}\n".format("\t".join(map(lambda a: str(a).strip(), d))))
                            f.close()

                        cd.is_dumped = YES
                        cd.save()

    def _fill_tables_columns(self):
        with connections['edxapp_readonly'].cursor() as cursor:
            for i in range(len(TABLES)):
                sql = "SHOW COLUMNS FROM edxapp.{table_name}".format(
                    table_name=TABLES[i]['name'],
                )
                cursor.execute(sql)
                TABLES[i]['columns'] = [str(row[0]) for row in cursor.fetchall()]

    def _dump_table(self, course, table, users):
        logger.info("dump course %s table %s", course, table['name'])
        with connections['edxapp_readonly'].cursor() as cursor:
            format_strings = ','.join(['%s'] * len(users))
            sql = "SELECT `{columns}` FROM edxapp.{table_name} WHERE {pk} IN(%s)".format(
                columns="`,`".join(table['columns']),
                table_name=table['name'],
                pk=table['pk']
            )
            cursor.execute(sql % format_strings, tuple(users))
            result = [list(row) for row in cursor.fetchall()]

            # remove passwords
            if 'password' in table['columns']:
                index = table['columns'].index('password')
                for i in range(len(result)):
                    result[i][index] = 'NULL'

            # table header
            result.insert(0, table['columns'])

            return result
        
    def _get_users(self, course):
        with connections['edxapp_readonly'].cursor() as cursor:
            cursor.execute("SELECT user_id FROM edxapp.student_courseenrollment WHERE course_id = %s", [course.name])
            return [row[0] for row in cursor.fetchall()]
