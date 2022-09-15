# -*- coding: utf-8 -*-
import datetime
import logging
import os
import shutil
import subprocess
from collections import defaultdict

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from split_logs.models import Organisation
from split_logs.utils import dump_course
from split_logs.utils import DumpCourseException
from split_logs.utils import run_command


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Course XML dump; running on one of the swarm server during the night'

    def handle(self, *args, **options):
        self.now = datetime.datetime.now().date()
        self.import_dir = '/var/lib/docker/volumes/openedx-{}_openedx-data/_data/course_export'

        course_data_for_email_ok = defaultdict(list)
        course_data_for_email_ko = defaultdict(list)

        organisations = Organisation.objects.filter(active=True)
        for org in organisations:
            logger.info("process organization %s", org.name)

            self.import_dir = self.import_dir.format(org.name.lower())

            # clean/create ogranigation destination directory
            org_destination_dir = self._handle_org_dir(org)

            for course_id in self._get_courses(org):
                logger.info('process course_id %s', course_id)
                try:
                    dump_course(org, course_id, org_destination_dir)
                    course_data_for_email_ok[org.name] += (course_id,)
                except DumpCourseException as e:
                    logger.error("Dump course exception: %s" % e)
                    course_data_for_email_ko[org.name] += (course_id,)

        self._send_email(course_data_for_email_ok, course_data_for_email_ko)

    def _handle_org_dir(self, org):
        org_destination_dir = '{}/{}/{}/'.format(
            settings.DUMP_XML_PATH,
            org.name.lower(),
            self.now
        )
        try:
            shutil.rmtree(org_destination_dir)
        except FileNotFoundError:
            pass

        # create directory
        os.mkdir(org_destination_dir)

        return org_destination_dir

    def _send_email(self, ok, ko):
        nok = sum([len(v) for v in ok.values()])
        nko = sum([len(v) for v in ko.values()])
        body = 'Course XML dump results - {}:\n\nDumped {} courses out of {}\n\nERRORS IN THE COURSES:\n{}'.format(
            self.now,
            nok,
            nok + nko
        )
        if nok > 0:
            body += '\n\nERRORS IN THE COURSES:\n{}'.format(
                '\n'.join(['\n' + k + ':\n' + '\n'.join(v) for k,v in ko.items()])
            )
        send_mail(
            '[SMS-extras:{env}] Course XML dump result - {date}'.format(
                env = settings.SMS_APP_ENV,
                date = self.now
            ),
            boby,
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
