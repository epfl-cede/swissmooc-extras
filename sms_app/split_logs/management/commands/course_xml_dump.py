import os
import shutil
import datetime
import logging
import gnupg

import boto3, botocore

from django.conf import settings
from django.core.management.base import BaseCommand

from split_logs.models import Organisation

BUCKET = settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Course XML dump; encrypt and upload course XMLs'

    def handle(self, *args, **options):
        organisations = Organisation.objects.all()

        now = datetime.datetime.now().date()
        dirs = [os.path.join(settings.DUMP_XML_PATH, o) for o in os.listdir(settings.DUMP_XML_PATH) if os.path.isdir(os.path.join(settings.DUMP_XML_PATH, o))]
        for cdir in dirs:
            logger.info('Process dir for encrypt %s', cdir)
            files = [os.path.join(cdir, o) for o in os.listdir(cdir) if not os.path.isdir(os.path.join(cdir, o)) and o.endswith('.zip')]

            for cfile in files:
                logger.info('Encrypt file %s', cfile)
                org = self._find_org_by_name(os.path.basename(cfile).split('-')[0])

                self._encrypt(org, cfile)

            logger.info('Process dir for upload %s', cdir)
            files = [os.path.join(cdir, o) for o in os.listdir(cdir) if not os.path.isdir(os.path.join(cdir, o)) and o.endswith('.gpg')]

            for efile in files:
                logger.info('Upload file %s', efile)
                org = self._find_org_by_name(os.path.basename(efile).split('-')[0])

                self._upload(org, efile)
                

    def _upload(self, org, ename):
        s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
        upload_file_name = '{org}/dump-xml/{date}/{name}'.format(
            org=org.name,
            date=ename.split('/')[-2],
            name=os.path.basename(ename)
        )
        fileinfo = os.stat(ename)
        try:
            head = s3.head_object(Bucket=BUCKET, Key=upload_file_name)
            # remove file if it has different size, it
            # will be uploaded next time script starts
            if  fileinfo.st_size != head['ContentLength']:
                logger.info("File %s has different size, remove it", ename)
                s3.delete_object(Bucket=BUCKET, Key=upload_file_name)
            else:
                logger.info("File exists; remove original")
                os.remove(ename)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                try:
                    logger.info("Upload file %s", upload_file_name)
                    s3.upload_file(ename, BUCKET, upload_file_name)
                    os.remove(ename)
                except Exception as e:
                    raise CommandError("Can not upload file %s: %s", upload_file_name, e)
            else:
                logger.info("File exists?")
        
    def _encrypt(self, org, fname):
        gpg = gnupg.GPG()
        gpg.encoding = 'utf-8'
        importres = gpg.import_keys(org.public_key.value)
        gpg.trust_keys(importres.fingerprints, 'TRUST_ULTIMATE')
        with open(fname, 'rb') as f:
            status = gpg.encrypt_file(
                f,
                armor=True,
                recipients=[org.public_key.recipient],
                output='{}.gpg'.format(fname),
            )
            if status.ok:
                logger.info("OK")
                os.remove(fname)
            else:
                logger.error("ERROR: %s", status.status)
                
    def _find_org_by_name(self, name):
        try:
            org = Organisation.objects.get(name=name);
        except Exception as e:
            print(e)
        return org
