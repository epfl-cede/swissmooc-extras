# -*- coding: utf-8 -*-
import logging
import os
import shutil

import gnupg
from apps.split_logs.models import CourseDump
from apps.split_logs.models import CourseDumpTable
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
from apps.split_logs.utils import upload_file
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(SMSCommand):
    help = "Course DB encrypt files"

    def handle(self, *args, **options):
        self.setOptions(**options)

        gpg = gnupg.GPG()
        gpg.encoding = "utf-8"
        organisations = Organisation.objects.filter(
            active=True,
            public_key__isnull=False,
        )
        tables = CourseDumpTable.objects.all()
        for org in organisations:
            logger.info(f"Process organisation <{org}>")
            cd = CourseDump.objects.filter(
                course__organisation=org,
                is_encypted=True,
                date=self.now
            )
            if len(cd) == 0:
                logger.warning("No course dumps")
            else:
                courses = org.course_set.filter(active=True)
                if len(cd) == len(courses) * len(tables):
                    folder_name = cd[0].dump_folder_name()
                    if os.path.isdir(folder_name):
                        zip_name = shutil.make_archive(
                            folder_name,
                            "zip",
                            os.path.dirname(folder_name),
                            os.path.basename(folder_name)
                        )
                    else:
                        zip_name = "{}.zip".format(folder_name)

                    if os.path.exists(zip_name):
                        bucker_filename = f"{org.name}/dump-db/{os.path.basename(zip_name)}"
                        logger.info(f"Upload file <{zip_name}> to <{bucker_filename}>")
                        upload_file(
                            org.bucket_name,
                            org,
                            zip_name,
                            bucker_filename,
                        )

                    if os.path.isdir(folder_name):
                        # remove original folder
                        shutil.rmtree(folder_name)
                else:
                    logger.warning(
                        f"Not all tables were dumped/encrypted, please check: organization <{org.name}>, date=<{self.now}>"
                    )
