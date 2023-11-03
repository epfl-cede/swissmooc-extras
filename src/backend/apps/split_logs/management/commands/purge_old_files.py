# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta

from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
from apps.split_logs.utils import s3_delete_file
from apps.split_logs.utils import s3_list_files

OLDER_THAN = datetime.now() - timedelta(days=90)
FOLDERS = [
    'dump-xml',
    'dump-db',
]


class Command(SMSCommand):
    help = "Purge old files"

    def handle(self, *args, **options):
        self.setOptions(**options)

        organisations = Organisation.objects.filter(
            active=True,
            public_key__isnull=False,
        )
        cnt_deleted = 0
        for org in organisations:
            for f in s3_list_files(org.bucket_name):
                fname = f['Key']
                fmdate = f['LastModified']
                for folder in FOLDERS:
                    if fname.find(f"/{folder}/") > 0 and fmdate.replace(tzinfo=None) < OLDER_THAN:
                        self._info(f"Delete file {fname}")
                        s3_delete_file(org.bucket_name, fname)
                        cnt_deleted += 1

        if cnt_deleted:
            self.send_email("Purge old files")
