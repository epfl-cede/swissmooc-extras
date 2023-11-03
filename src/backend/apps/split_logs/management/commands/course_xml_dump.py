# -*- coding: utf-8 -*-
import os
import shutil
from collections import defaultdict
from datetime import datetime

import gnupg
from apps.split_logs.models import Course
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
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
    help = "Course XML dump, save it to S3, extract course structure"

    def add_arguments(self, parser):
        parser.add_argument('--org', type=str, default="")
        parser.add_argument('--course_id', type=str, default="")

    def handle(self, *args, **options):
        self.setOptions(**options)

        if options['org'] and options['course_id']:
            self.handle_course(options['org'], options['course_id'])
        elif options['org']:
            self.handle_org(options['org'])
        else:
            self.handle_all_courses()

    def handle_course(self, org: str, course_id: str):
        org = Organisation.objects.get(active=True, name=org)
        self._info(f"organisation: {org.name}")
        self._info(f"course: {course_id}")

        # clean/create ogranigation destination directory
        org_destination_dir = self._dump_dir(org)
        self._create_org_dir(org_destination_dir)

        try:
            course_file = dump_course(org, course_id, org_destination_dir)
            self._updateCourseStructure(org, course_id, course_file)
            self._info(f"{course_id=} {course_file=}")
        except SplitLogsUtilsDumpCourseException:
            self._warning(f"{course_id=} not found")

    def handle_org(self, org: str):
        try:
            Org = Organisation.objects.get(active=True, name=org)
        except ObjectDoesNotExist:
            raise CourseXmlDumpException(f"Organisation {org=} doesn't exists")

        ok, ko = self._process_org(Org)
        self._send_email(ok, ko)

    def handle_all_courses(self):
        course_data_for_email_ok = defaultdict(list)
        course_data_for_email_ko = defaultdict(list)

        organisations = Organisation.objects.filter(active=True)
        for org in organisations:
            ok, ko = self._process_org(org)
            course_data_for_email_ok.update(ok)
            course_data_for_email_ko.update(ko)

        self._send_email(course_data_for_email_ok, course_data_for_email_ko)

    def _process_org(self, org: Organisation):
        self._info(f"organisation: {org.name}")

        # clean/create ogranigation destination directory
        org_destination_dir = self._dump_dir(org)
        self._create_org_dir(org_destination_dir)

        ok, ko = defaultdict(list), defaultdict(list)
        for course_id in self._get_courses(org):
            self._info(f"course: {course_id}")
            try:
                course_file = dump_course(
                    org,
                    course_id,
                    org_destination_dir
                )
                self._updateCourseStructure(org, course_id, course_file)
                if org.public_key:
                    course_file_encrypted = self._encrypt(org, course_file)
                    self._upload(org, course_file_encrypted)
                else:
                    self._upload(org, course_file)
                ok[org.name] += (course_id,)
            except SplitLogsUtilsDumpCourseException as error:
                self._error(f"dump course: <{error}>")
                ko[org.name] += (course_id,)
            except SplitLogsUtilsUploadFileException as error:
                self._error(f"upload: <{error}>")
                ko[org.name] += (course_id,)
            except CourseXmlDumpException as error:
                self._error(f"script exception: <{error}>")
                ko[org.name] += (course_id,)
        return ok, ko

    def _updateCourseStructure(self, org, course_id, course_file):
        try:
            course = Course.objects.get(organisation=org, course_id=course_id)
            course.structure = course_structure.structure(course_file)
            course.save()
        except course_structure.OpenEdxCourseStructureException as error:
            raise CourseXmlDumpException(f"Course {course_id=} structure exception {error=}")
        except ObjectDoesNotExist:
            raise CourseXmlDumpException(f"Course {course_id=} doesn't exists")

    def _upload(self, org, fname):
        upload_file(
            org.bucket_name,
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
            self._error(f"get course list error: <{stderr}>")
            return []

        return stdout.strip("\n").split("\n")[1:]

    def _message(self, message, level):
        now = datetime.now()
        self.message.append(f"[{now:%Y-%m-%d %H:%M}] {level} {message}")
