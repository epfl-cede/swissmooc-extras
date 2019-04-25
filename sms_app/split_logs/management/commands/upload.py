import logging
import boto3, botocore
import os
from dateutil import parser

from split_logs.models import Organisation

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Encrypt files with organization keys and put it on SWITCH Drive'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)

    def handle(self, *args, **options):
        limit = options['limit']
        cnt = 0
        s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
        try:
            response = s3.list_buckets()
        except Exception as e:
            raise CommandError("SWICH Containers error: '%s'", e)
        if settings.AWS_STORAGE_BUCKET_NAME not in map(lambda i: i['Name'], response['Buckets']):
            raise CommandError("Can not fine bucket %s", settings.AWS_STORAGE_BUCKET_NAME)

        organisations = Organisation.objects.all()
        for o in organisations:
            aliases = o.aliases.split(',')
            for a in aliases:
                org = a.strip()
                logger.info("process organisation alias '{}'".format(org))
                filelist = self._get_list(org)
                for encripted_file in filelist:
                    encripted_file = '{}/{}'.format(org, encripted_file)
                    encripted_file_full_path = "{}/{}".format(settings.TRACKING_LOGS_ENCRYPTED, encripted_file)
                    fileinfo = os.stat(encripted_file_full_path)
                    try:
                        head = s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=encripted_file)
                        # remove file if it has different size, it
                        # will be uploaded next time script starts
                        if  fileinfo.st_size != head['ContentLength']:
                            logger.info("File %s has different size, remove it", encripted_file)
                            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=encripted_file)
                    except botocore.exceptions.ClientError as e:
                        if e.response['Error']['Code'] == "404":
                            try:
                                logger.info("Uploda file %s", encripted_file)
                                response = s3.upload_file(encripted_file_full_path, settings.AWS_STORAGE_BUCKET_NAME, encripted_file)
                            except Exception as e:
                                raise CommandError("Can not upload file %s: %s", encripted_file, e)
                        else:
                            logger.info("File exists")
                            
                    
    def _get_list(self, org):
        files = list()
        try:
            path = "{}/{}".format(settings.TRACKING_LOGS_ENCRYPTED, org)
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except FileNotFoundError:
            logger.warning("organisation '%s' folder does not exist", org)
        return files
