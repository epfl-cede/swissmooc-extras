import os
import datetime
import logging
import gnupg
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from split_logs.utils import upload_file
from split_logs.models import CourseDump, Organisation, CourseDumpTable
from split_logs.models import ACTIVE, YES

LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Course DB encrypt files'

    def handle(self, *args, **options):
        cnt = 0

        gpg = gnupg.GPG()
        gpg.encoding = 'utf-8'
        organisations = Organisation.objects.filter(active=True)
        tables = CourseDumpTable.objects.all()
        now = datetime.datetime.now().date()
        for org in organisations:
            LOGGER.info("Process organisation %s", org.name)
            cd = CourseDump.objects.filter(course__organisation=org, is_encypted=YES, date=now)
            if len(cd) == 0:
                LOGGER.warning("No course dumps")
            else:
                courses = org.course_set.filter(active=ACTIVE)
                if len(cd) == len(courses) * len(tables):
                    folder_name = cd[0].dump_folder_name()
                    if os.path.isdir(folder_name):
                        zip_name = shutil.make_archive(folder_name, 'zip', os.path.dirname(folder_name), os.path.basename(folder_name))
                    else:
                        zip_name = '{}.zip'.format(folder_name)

                    if os.path.exists(zip_name):
                        LOGGER.info('Upload file %s to %s', zip_name, '{org}/dump-db/{name}'.format(
                            org=org.name,
                            name=os.path.basename(zip_name),
                        ))
                        upload_file(
                            settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS,
                            org,
                            zip_name,
                            '{org}/dump-db/{name}'.format(
                                org=org.name,
                                name=os.path.basename(zip_name),
                            )
                        )

                    if os.path.isdir(folder_name):
                        # remove original folder
                        shutil.rmtree(folder_name)
                else:
                    LOGGER.warning("Not all tables were dumped/encrypted, please check: organization=%s, date=%s", org.name, now)
