import logging
import os
from dateutil import parser

import boto3, botocore

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from split_logs.models import Organisation

logger = logging.getLogger(__name__)

BUCKET = settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS

class Command(BaseCommand):
    help = 'Encrypt files with organization keys and put it on SWITCH Drive'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=100)

    def handle(self, *args, **options):
        limit = options['limit']
        cnt = 0
        s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
        try:
            response = s3.list_buckets()
        except Exception as e:
            raise CommandError("SWICH Containers error: '%s'", e)
        if BUCKET not in map(lambda i: i['Name'], response['Buckets']):
            raise CommandError("Can not fine bucket %s", BUCKET)

        organisations = Organisation.objects.all()
        for o in organisations:
            aliases = o.aliases.split(',')
            for a in aliases:
                org = a.strip()
                logger.info("process organisation alias '{}'".format(org))
                filelist = self._get_list(org)
                for encripted_file in filelist:
                    upload_file_path = '{}/tracking-logs/{}'.format(org, encripted_file)
                    encripted_file_full_path = "{}/{}/{}".format(settings.TRACKING_LOGS_ENCRYPTED, org, encripted_file)
                    fileinfo = os.stat(encripted_file_full_path)
                    try:
                        head = s3.head_object(Bucket=BUCKET, Key=upload_file_path)
                        # remove file if it has different size, it
                        # will be uploaded next time script starts
                        if  fileinfo.st_size != head['ContentLength']:
                            logger.info("File %s has different size, remove it", upload_file_path)
                            s3.delete_object(Bucket=BUCKET, Key=upload_file_path)
                    except botocore.exceptions.ClientError as e:
                        if e.response['Error']['Code'] == "404":
                            try:
                                logger.info("Upload file %s/%s", org, encripted_file)
                                response = s3.upload_file(encripted_file_full_path, BUCKET, upload_file_path)
                                cnt += 1
                            except Exception as e:
                                raise CommandError("Can not upload file %s: %s", upload_file_path, e)
                        else:
                            logger.info("File exists")

                    if cnt >= limit: break
                if cnt >= limit: break
            if cnt >= limit: break
                            
                    
    def _get_list(self, org):
        files = list()
        try:
            path = "{}/{}".format(settings.TRACKING_LOGS_ENCRYPTED, org)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except FileNotFoundError:
            logger.warning("organisation '%s' folder does not exist", org)
        return files
