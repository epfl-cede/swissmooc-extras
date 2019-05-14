import os
import datetime
import logging
import gnupg
import shutil

import boto3, botocore

from django.conf import settings
from django.db import connections
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from split_logs.models import Course, CourseDump, Organisation, CourseDumpTable
from split_logs.models import ACTIVE, NOT_ACTIVE, YES, NO

logger = logging.getLogger(__name__)

BUCKET = settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS

class Command(BaseCommand):
    help = 'Course DB encrypt files'

    def handle(self, *args, **options):
        cnt = 0

        gpg = gnupg.GPG()
        gpg.encoding = 'utf-8'
        organisations = Organisation.objects.all()
        tables = CourseDumpTable.objects.all()
        now = datetime.datetime.now().date()
        s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
        for org in organisations:
            logger.info("Process organisation %s", org.name)
            cd = CourseDump.objects.filter(course__organisation=org, is_encypted=YES, date=now)
            if len(cd) == 0:
                logger.warning("No course dumps")
            else:
                courses = org.course_set.filter(active=ACTIVE)
                if len(cd) == len(courses) * len(tables):
                    folder_name = cd[0].dump_folder_name()
                    zip_name = shutil.make_archive(folder_name, 'zip', os.path.dirname(folder_name), os.path.basename(folder_name))
                    upload_file_name = '{org}/dump-db/{name}'.format(org=org.name, name=os.path.basename(zip_name))
                    fileinfo = os.stat(zip_name)
                    try:
                        head = s3.head_object(Bucket=BUCKET, Key=upload_file_name)
                        # remove file if it has different size, it
                        # will be uploaded next time script starts
                        if  fileinfo.st_size != head['ContentLength']:
                            logger.info("File %s has different size, remove it", zip_name)
                            s3.delete_object(Bucket=BUCKET, Key=upload_file_name)
                    except botocore.exceptions.ClientError as e:
                        if e.response['Error']['Code'] == "404":
                            try:
                                logger.info("Upload file %s", upload_file_name)
                                response = s3.upload_file(zip_name, BUCKET, upload_file_name)
                                cnt += 1
                            except Exception as e:
                                raise CommandError("Can not upload file %s: %s", upload_file_name, e)
                        else:
                            logger.info("File exists")
                else:
                    logger.warning("Not all tables were dumped/encrypted, please check: organization=%s, date=%s", org.name, now)
            
            
