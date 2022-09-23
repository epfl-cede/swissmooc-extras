# -*- coding: utf-8 -*-
import datetime
import logging
import os
import shutil

import gnupg
from django.conf import settings
from split_logs.models import ACTIVE
from split_logs.models import CourseDump
from split_logs.models import CourseDumpTable
from split_logs.models import Organisation
from split_logs.models import YES
from split_logs.sms_command import SMSCommand
from split_logs.utils import bucket_name
from split_logs.utils import upload_file


class Command(SMSCommand):
    help = "Course DB encrypt files"
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.handle_verbosity(options)

        gpg = gnupg.GPG()
        gpg.encoding = "utf-8"
        organisations = Organisation.objects.filter(active=True)
        tables = CourseDumpTable.objects.all()
        for org in organisations:
            self.info(f"Process organisation <{org}>")
            cd = CourseDump.objects.filter(course__organisation=org, is_encypted=YES, date=self.now)
            if len(cd) == 0:
                self.warning("No course dumps")
            else:
                courses = org.course_set.filter(active=ACTIVE)
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
                        self.info(f"Upload file <{zip_name}> to <{bucker_filename}>")
                        upload_file(
                            bucket_name(org),
                            org,
                            zip_name,
                            bucker_filename,
                        )

                    if os.path.isdir(folder_name):
                        # remove original folder
                        shutil.rmtree(folder_name)
                else:
                    self.warning(
                        f"Not all tables were dumped/encrypted, please check: organization <{org.name}>, date=<{self.now}>"
                    )
