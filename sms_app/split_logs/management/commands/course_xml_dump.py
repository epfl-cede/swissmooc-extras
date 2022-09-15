# -*- coding: utf-8 -*-
import datetime
import logging
import os
import shutil
import subprocess
from collections import defaultdict

import gnupg
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from split_logs.models import Organisation
from split_logs.utils import bucket_name
from split_logs.utils import dump_course
from split_logs.utils import run_command
from split_logs.utils import SplitLogsUtilsDumpCourseException
from split_logs.utils import SplitLogsUtilsUploadFileException
from split_logs.utils import upload_file


logger = logging.getLogger(__name__)

class CourseXmlDumpException(Exception):
    """Base class for other exceptions"""
    pass

class Command(BaseCommand):
    help = 'Course XML dump; running on one of the swarm server during the night'

    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', help='Debug info')

    def handle(self, *args, **options):
        self.now = datetime.datetime.now().date()

        course_data_for_email_ok = defaultdict(list)
        course_data_for_email_ko = defaultdict(list)

        organisations = Organisation.objects.filter(active=True)
        for org in organisations:
            logger.info("process organisation %s", org.name)

            self.import_dir = '/var/lib/docker/volumes/openedx-{}_openedx-data/_data/course_export'.format(
                org.name.lower()
            )

            # clean/create ogranigation destination directory
            org_destination_dir = self._organisation_dir(org)
            self._create_org_dir(org_destination_dir)

            for course_id in self._get_courses(org):
                logger.info('process course_id %s', course_id)
                try:
                    course_file = dump_course(org, course_id, org_destination_dir)
                    course_file_encrypted = self._encrypt(org, course_file)
                    self._upload(org, course_file_encrypted)
                    course_data_for_email_ok[org.name] += (course_id,)
                except SplitLogsUtilsDumpCourseException as error:
                    logger.error("SplitLogsUtilsDumpCourseException: %s" % error)
                    course_data_for_email_ko[org.name] += (course_id,)
                except SplitLogsUtilsUploadFileException as error:
                    logger.error("SplitLogsUtilsUploadFileException: %s" % error)
                    course_data_for_email_ko[org.name] += (course_id,)
                except CourseXmlDumpException as error:
                    logger.error("CourseXmlDumpException: %s" % error)
                    course_data_for_email_ko[org.name] += (course_id,)

        self._send_email(course_data_for_email_ok, course_data_for_email_ko)

    def _upload(self, org, fname):
        upload_file(
            bucket_name(org),
            org,
            fname,
            '{org}/dump-xml/{date}/{name}'.format(
                org=org.name,
                date=fname.split('/')[-2],
                name=os.path.basename(fname)
            )
        )

    def _encrypt(self, org, fname):
        gpg = gnupg.GPG()
        gpg.encoding = 'utf-8'
        importres = gpg.import_keys(org.public_key.value)
        gpg.trust_keys(importres.fingerprints, 'TRUST_ULTIMATE')
        fname_encrypted = '{}.gpg'.format(fname)
        with open(fname, 'rb') as f:
            status = gpg.encrypt_file(
                f,
                armor=True,
                recipients=[org.public_key.recipient],
                output=fname_encrypted,
            )
            if status.ok:
                os.remove(fname)
            else:
                raise CourseXmlDumpException('Encrypt file error')
        return fname_encrypted

    def _organisation_dir(self, organisation):
        return '{}/{}/{}/'.format(
            settings.DUMP_XML_PATH,
            organisation.name.lower(),
            self.now
        )

    def _create_org_dir(self, organisation_dir):
        try:
            shutil.rmtree(organisation_dir)
        except FileNotFoundError:
            pass

        # create directory
        os.makedirs(organisation_dir)

    def _send_email(self, ok, ko):
        nok = sum([len(v) for v in ok.values()])
        nko = sum([len(v) for v in ko.values()])
        body = 'Course XML dump results - {}:\n\nDumped {} courses out of {}'.format(
            self.now,
            nok,
            nok + nko
        )
        if nko > 0:
            body += '\n\nERRORS IN THE COURSES:\n{}'.format(
                '\n'.join(['\n' + k + ':\n' + '\n'.join(v) for k,v in ko.items()])
            )
        send_mail(
            '[SMS-extras:{env}] Course XML dump result - {date}'.format(
                env = settings.SMS_APP_ENV,
                date = self.now
            ),
            body,
            settings.EMAIL_FROM_ADDRESS,
            settings.EMAIL_TO_ADDRESSES,
            fail_silently=False,
        )

    def _get_courses(self, org):
        return_code, stdout, stderr = run_command([
            'ssh', 'ubuntu@zh-%s-swarm-1' % settings.SMS_APP_ENV,
            '/home/ubuntu/.local/bin/docker-run-command', 'openedx-%s_cms' % org.name.lower(),
            'python', 'manage.py', 'cms', '--settings=tutor.production', 'dump_course_ids'
        ])
        if return_code != 0:
            logger.error('get course list error: %s', stderr)
            return []

        return stdout.decode().strip('\n').split('\n')[1:]
