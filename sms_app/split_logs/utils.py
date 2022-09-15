# -*- coding: utf-8 -*-
import logging
import os
import shutil
import subprocess
import tempfile

import boto3
import botocore
from django.conf import settings

LOGGER = logging.getLogger(__name__)

def upload_file(bucket, organisation, original_name, upload_name):
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
        head = s3.head_object(Bucket=bucket, Key=upload_name)
        # remove file if it has different size(more than 10 bytes)
        # this is real example local = 237996, remote = 238000
        # s3.head_object sometime returns slightly different filesize,
        # though downloaded file has exactly the same as local file size.
        if  max(fileinfo.st_size, head['ContentLength']) - min(fileinfo.st_size, head['ContentLength']) > 10:
            LOGGER.error("File %s has different size(local = %d against remote = %d), remove it", original_name, fileinfo.st_size, head['ContentLength'])
            s3.delete_object(Bucket=bucket, Key=upload_name)
            # re-upload it
            upload_file(organisation, original_name, upload_name)
        else:
            os.remove(original_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            try:
                s3.upload_file(original_name, bucket, upload_name)
                os.remove(original_name)
                LOGGER.info("file '%s' uploaded", original_name)
            except Exception as e:
                raise Exception("Can not upload file %s: %s", upload_name, e)
        else:
            LOGGER.error("File exists? (%s)", e)

def run_command(cmd):
    LOGGER.debug('Run command: {}'.format(cmd))
    process = subprocess.Popen(
        cmd,
        shell = False,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    return_code = process.returncode

    return return_code, stdout, stderr


class DumpCourseException(Exception):
    """Base class for other exceptions"""
    pass

def dump_course(organization, course_id, destination_folder):
    """
    Creates zip archive of the exported course in the specified folder
    """

    organization_name = organization.name.lower()
    container_name = 'openedx-%s_cms' % organization_name
    container_host = 'ubuntu@zh-%s-swarm-1' % settings.SMS_APP_ENV
    cmd = [
        'ssh', container_host,
    ]
    cmd_container = cmd + [
        '/home/ubuntu/.local/bin/docker-run-command', container_name
    ]
    import_folder_container = '/openedx/data/course_export/course'
    import_folder = '/var/lib/docker/volumes/openedx-%s_openedx-data/_data/course_export' % organization_name

    # Export course
    return_code, stdout, stderr = run_command(cmd_container + [
        'rm', '-rf', import_folder_container
    ])
    if return_code != 0:
        raise DumpCourseException('clean course export directory error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd_container + [
        'mkdir', '-p', import_folder_container
    ])
    if return_code != 0:
        raise DumpCourseException('clean course export directory error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd_container + [
        'python', 'manage.py', 'cms', '--settings=tutor.production', 'export', course_id, import_folder_container
    ])
    if return_code != 0:
        raise DumpCourseException('course export error: %s', stderr)

    # Move course to temporary folder
    tmp_folder = '/tmp/course_export'
    return_code, stdout, stderr = run_command(cmd + [
        'sudo', 'rm', '-Rf', tmp_folder
    ])
    if return_code != 0:
        raise DumpCourseException('remove tmp folder error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd + [
        'mkdir', '-p', tmp_folder
    ])
    if return_code != 0:
        raise DumpCourseException('make tmp folder error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd + [
        'sudo', 'mv', import_folder, '/tmp/'
    ])
    if return_code != 0:
        raise DumpCourseException('move course to tmp folder error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd + [
        'sudo', 'chown', '-R', 'ubuntu:ubuntu', tmp_folder
    ])
    if return_code != 0:
        raise DumpCourseException('chown tmp folder error: %s', stderr)

    # Make archive & move course to the destination folder
    course_destination_folder = destination_folder + course_id[10:]
    os.makedirs(course_destination_folder, exist_ok=True)

    return_code, stdout, stderr = run_command([
        'rsync', '-avz', container_host + ':' + tmp_folder + '/', course_destination_folder
    ])
    if return_code != 0:
        raise DumpCourseException('course rsync error: %s', stderr)

    zip_name = shutil.make_archive(
        course_destination_folder,
        'gztar',
        course_destination_folder
    )
    shutil.rmtree(course_destination_folder)
