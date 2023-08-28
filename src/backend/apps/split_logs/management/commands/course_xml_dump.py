# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import shutil
import subprocess
from collections import defaultdict

import gnupg
from apps.split_logs.models import Course
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
from apps.split_logs.utils import bucket_name
from apps.split_logs.utils import dump_course
from apps.split_logs.utils import run_command
from apps.split_logs.utils import SplitLogsUtilsDumpCourseException
from apps.split_logs.utils import SplitLogsUtilsUploadFileException
from apps.split_logs.utils import upload_file
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from openedx_course_structure import course_structure


class CourseXmlDumpException(Exception):
    """Base class for other exceptions"""
    pass


class Command(SMSCommand):
    help = "Course XML dump; running on one of the swarm server during the night"

    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('--course_id', type=str, default="")

    def handle(self, *args, **options):
        self.handle_verbosity(options)

        if options['course_id'] == "":
            self.handle_all_courses()
        else:
            self.handle_course(options['course_id'])

    def handle_course(self, course_id):
        organisations = Organisation.objects.filter(active=True)
        for org in organisations:
            self.info(f"organisation: {org.name}")

            # clean/create ogranigation destination directory
            org_destination_dir = self._dump_dir(org)
            self._create_org_dir(org_destination_dir)

            try:
                course_file = dump_course(org, course_id, org_destination_dir)
                self._updateCourseStructure(org, course_id, course_file)
                self.info(f"course: {course_id}")
                self.info(f"see: {course_file}")
            except SplitLogsUtilsDumpCourseException:
                self.warning(f"Course not found: {course_id}")

    def handle_all_courses(self):
        course_data_for_email_ok = defaultdict(list)
        course_data_for_email_ko = defaultdict(list)

        organisations = Organisation.objects.filter(active=True)
        for org in organisations:
            self.info(f"organisation: {org.name}")

            # clean/create ogranigation destination directory
            org_destination_dir = self._dump_dir(org)
            self._create_org_dir(org_destination_dir)

            for course_id in self._get_courses(org):
                self.info(f"course: {course_id}")
                try:
                    course_file = dump_course(org, course_id, org_destination_dir)
                    self._updateCourseStructure(org, course_id, course_file)
                    course_file_encrypted = self._encrypt(org, course_file)
                    self._upload(org, course_file_encrypted)
                    course_data_for_email_ok[org.name] += (course_id,)
                except SplitLogsUtilsDumpCourseException as error:
                    self.error(f"dump course: <{error}>")
                    course_data_for_email_ko[org.name] += (course_id,)
                except SplitLogsUtilsUploadFileException as error:
                    self.error(f"upload: <{error}>")
                    course_data_for_email_ko[org.name] += (course_id,)
                except CourseXmlDumpException as error:
                    self.error(f"script exception: <{error}>")
                    course_data_for_email_ko[org.name] += (course_id,)

        self._send_email(course_data_for_email_ok, course_data_for_email_ko)

    def _updateCourseStructure(self, org, course_id, course_file):
        try:
            course = Course.objects.get(organisation=org, course_id=course_id)
            course.structure = course_structure.structure(course_file)
            course.save()
        except ObjectDoesNotExist:
            raise CourseXmlDumpException(f"Course {course_id=} doesn't exists")

    def _upload(self, org, fname):
        upload_file(
            bucket_name(org),
            org,
            fname,
            "{org}/dump-xml/{date}/{name}".format(
                org=org.name,
                date=fname.split("/")[-2],
                name=os.path.basename(fname)
            )
        )

    def _encrypt(self, org, fname):
        gpg = gnupg.GPG()
        gpg.encoding = "utf-8"
        gpg.import_keys(org.public_key.value)
        fname_encrypted = "{}.gpg".format(fname)
        with open(fname, "rb") as f:
            status = gpg.encrypt_file(
                f,
                armor=True,
                recipients=[org.public_key.recipient],
                output=fname_encrypted,
            )
            if status.ok:
                os.remove(fname)
            else:
                raise CourseXmlDumpException("Encrypt file error")
        return fname_encrypted

    def _dump_dir(self, organisation):
        return "{}/{}".format(
            self._organisation_dir(organisation),
            self.now
        )

    def _structure_dir(self, organisation):
        return "{}/{}".format(
            self._organisation_dir(organisation),
            'structure'
        )

    def _organisation_dir(self, organisation):
        return "{}/{}".format(
            settings.DUMP_XML_PATH,
            organisation.name.lower(),
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
        result_message = []
        result_message.append(f"{nok} courses were dumped out of {nok + nko}")
        if nko > 0:
            result_message.append("There are errors in the courses below:")
            for org, courses in ko.items():
                result_message.append(f"{org}")
                for course in courses:
                    result_message.append(f"{course}")

        result_message.append("")
        result_message.append("Detailed log:")

        self.message = result_message + self.message

        self.send_email("Course XML dump")

    def _get_courses(self, org):
        return_code, stdout, stderr = run_command([
            "ssh", "ubuntu@zh-%s-swarm-1" % settings.SMS_APP_ENV,
            "/home/ubuntu/.local/bin/docker-run-command", "openedx-%s_cms" % org.name.lower(),
            "python", "manage.py", "cms", "--settings=tutor.production", "dump_course_ids"
        ])
        if return_code != 0:
            self.error(f"get course list error: <{stderr}>")
            return []

        return stdout.strip("\n").split("\n")[1:]
