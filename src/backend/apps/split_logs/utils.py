# -*- coding: utf-8 -*-
import logging
import os
import shutil
import subprocess

import boto3
import botocore
from django.conf import settings

logger = logging.getLogger(__name__)


class SplitLogsUtilsException(Exception):
    """Base class for other exceptions"""
    pass


class SplitLogsUtilsDumpCourseException(SplitLogsUtilsException):
    """Base class for other exceptions"""
    pass


class SplitLogsUtilsUploadFileException(SplitLogsUtilsException):
    """Base class for other exceptions"""
    pass


def s3_list_files(bucket):
    s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
    logger.debug(f"List files in the {bucket=}")
    response = s3.list_objects_v2(Bucket=bucket)
    return response.get("Contents")


def s3_delete_file(bucket, fname):
    s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
    logger.debug(f"Delete {fname=} from the {bucket=}")
    s3.delete_object(Bucket=bucket, Key=fname)


def s3_upload_file(bucket, organisation, original_name, upload_name):
    s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL"))
    logger.debug('Upload file %s to %s', original_name, upload_name)

    fileinfo = os.stat(original_name)
    try:
        head = s3.head_object(Bucket=bucket, Key=upload_name)
        # remove file if it has different size(more than 10 bytes)
        # this is real example local = 237996, remote = 238000
        # s3.head_object sometime returns slightly different filesize,
        # though downloaded file has exactly the same as local file size.
        diff = max(
            fileinfo.st_size, head['ContentLength']
        ) - min(
            fileinfo.st_size, head['ContentLength']
        )
        if diff > 10:
            logger.warning(
                f"File {original_name=} has different size"
                f"(local={fileinfo.st_size}, "
                f"remote={head['ContentLength']}), replace it"
            )
            s3.delete_object(Bucket=bucket, Key=upload_name)
            # re-upload it
            s3_upload_file(bucket, organisation, original_name, upload_name)
        else:
            os.remove(original_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            try:
                s3.upload_file(original_name, bucket, upload_name)
                os.remove(original_name)
                logger.info("file '%s' uploaded", original_name)
            except botocore.exceptions.ClientError as error:
                raise SplitLogsUtilsUploadFileException(
                    f"Upload file exception <{upload_name=}>: {error=}"
                )
        else:
            logger.error("File exists? (%s)", e)


def run_command(cmd):
    logger.debug(f"Run command: <{' '.join(cmd)}>")
    process = subprocess.Popen(
        cmd,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    return_code = process.returncode

    stdout = stdout.strip().decode("utf-8")
    stderr = stderr.strip().decode("utf-8")
    return return_code, stdout, stderr


def dump_course(organization, course_id, destination_folder):
    """
    Creates zip archive of the exported course in the specified folder
    """

    organization_name = organization.name.lower()
    container_name = 'openedx-%s_cms-worker' % organization_name

    # find swarm server where cms-worker is located
    return_code, stdout, stderr = run_command([
        'ssh', 'ubuntu@zh-%s-swarm-1' % settings.SMS_APP_ENV,
        'docker', 'service', 'ps', container_name, '--filter', 'desired-state=running'
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException(
            f"could not get VM with {container_name=} service: {stderr=}"
        )

    try:
        container_host = 'ubuntu@%s' % stdout.split('\n')[1].split()[3]
    except IndexError:
        raise SplitLogsUtilsDumpCourseException(f"failed to parse VM from the string: {stdout=}")

    cmd = ['ssh', container_host]
    cmd_container = cmd + [
        '/home/ubuntu/.local/bin/docker-run-command', container_name
    ]
    import_folder_container = '/openedx/data/export/course_export/course'
    import_folder = f"/var/lib/docker/volumes/openedx-{organization_name}_openedx-data/_data/export/course_export"

    # Export course
    return_code, stdout, stderr = run_command(cmd_container + [
        'rm', '-rf', import_folder_container
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException('clean course export directory error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd_container + [
        'mkdir', '-p', import_folder_container
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException('make directory error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd_container + [
        'python', 'manage.py', 'cms', '--settings=tutor.production', 'export', course_id, import_folder_container
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException('course export error: %s', stderr)

    # Move course to temporary folder
    tmp_folder = '/tmp/course_export'
    return_code, stdout, stderr = run_command(cmd + [
        'sudo', 'rm', '-Rf', tmp_folder
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException('remove tmp folder error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd + [
        'mkdir', '-p', tmp_folder
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException('make tmp folder error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd + [
        'sudo', 'mv', import_folder, '/tmp/'
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException('move course to tmp folder error: %s', stderr)

    return_code, stdout, stderr = run_command(cmd + [
        'sudo', 'chown', '-R', 'ubuntu:ubuntu', tmp_folder
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException(
            'chown tmp folder error: %s',
            stderr
        )

    # Make archive & move course to the destination folder
    course_destination_folder = destination_folder + '/' + course_id[10:]
    os.makedirs(course_destination_folder, exist_ok=True)

    return_code, stdout, stderr = run_command([
        'rsync', '-avz', container_host + ':' + tmp_folder + '/', course_destination_folder
    ])
    if return_code != 0:
        raise SplitLogsUtilsDumpCourseException(
            'course rsync error: %s',
            stderr
        )

    shutil.make_archive(
        course_destination_folder,
        'gztar',
        course_destination_folder
    )
    shutil.rmtree(course_destination_folder)

    return course_destination_folder + '.tar.gz'
