import os
import datetime
import logging
import pathlib

from django.conf import settings
from django.db import connections
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from split_logs.models import Course, Organisation, ACTIVE, NOT_ACTIVE

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
        organisations = Organisation.objects.all()
        for o in organisations:
            logger.info("process organization %s", o.name)
            for course in o.course_set.filter(active=ACTIVE):
                users = self._get_users(course)
                for table in TABLES:
                    data = self._dump_table(course, table, users)
                    file_name = self._get_dump_file_full_path(o, course, table)
                    pathlib.Path(os.path.dirname(file_name)).mkdir(parents=True, exist_ok=True)
                    logger.info("dump %s table into %s", table['name'], file_name)
                    with open(file_name, 'w') as f:
                        for d in data:
                            f.write("{}\n".format("\t".join(map(lambda a: str(a).strip(), d))))
                    f.close()
                break
            break

    def _get_dump_file_full_path(self, organisation, course, table):
        #epflx-2019-04-21/EPFLx-Algebre2X-1T2017-auth_user-prod-analytics.sql.gpg
        return "{path}/{org_name}/{date}/{org_name_lower}x-{date}/{course_folder}-{table_name}-prod-analytics.sql".format(
            path=settings.DUMP_DB_RAW,
            org_name=organisation.name,
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
            course_folder=course.folder,
            org_name_lower=organisation.name.lower(),
            table_name=table['name'],
        )

    def _dump_table(self, course, table, users):
        logger.info("dump course %s table %s", course, table['name'])
        with connections['edxapp_readonly'].cursor() as cursor:
            sql = "SHOW COLUMNS FROM edxapp.{table_name}".format(
                table_name=table['name'],
            )
            cursor.execute(sql)
            columns = [row[0] for row in cursor.fetchall()]

            sql = "SELECT `{columns}` FROM edxapp.{table_name} WHERE {pk} IN(%s)".format(
                columns="`,`".join(columns),
                table_name=table['name'],
                pk=table['pk']
            )
            cursor.execute(sql, [users])
            result = [list(row) for row in cursor.fetchall()]

            # remove passwords
            if 'password' in columns:
                index = columns.index('password')
                for i in range(len(result)):
                    result[i][index] = 'NULL'

            # table header
            result.insert(0, columns)

            return result
        
    def _get_users(self, course):
        with connections['edxapp_readonly'].cursor() as cursor:
            cursor.execute("SELECT user_id FROM edxapp.student_courseenrollment WHERE course_id = %s", [course.name])
            return [row[0] for row in cursor.fetchall()]
