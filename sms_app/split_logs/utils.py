import os
import logging
import boto3, botocore

from django.conf import settings

LOGGER = logging.getLogger(__name__)

def upload_file(organisation, original_name, upload_name):
    s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
    LOGGER.debug('Upload file %s to %s', original_name, upload_name)

    # don't need to check it before copy each file
    #
    #try:
    #    response = s3.list_buckets()
    #except Exception as e:
    #    raise Exception("SWICH Containers error: '%s'", e)
    #if settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS not in map(lambda i: i['Name'], response['Buckets']):
    #    raise Exception("Can not fine bucket %s", settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS)

    fileinfo = os.stat(original_name)
    try:
        head = s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS, Key=upload_name)
        # remove file if it has different size, it
        # will be uploaded next time script starts
        if  fileinfo.st_size != head['ContentLength']:
            LOGGER.error("File %s has different size, remove it", original_name)
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS, Key=upload_name)
        else:
            os.remove(original_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            try:
                s3.upload_file(original_name, settings.AWS_STORAGE_BUCKET_NAME_ANALYTICS, upload_name)
                os.remove(original_name)
            except Exception as e:
                raise Exception("Can not upload file %s: %s", upload_name, e)
        else:
            LOGGER.error("File exists? (%s)", e)
