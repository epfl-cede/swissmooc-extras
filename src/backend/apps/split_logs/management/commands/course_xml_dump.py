# -*- coding: utf-8 -*-
import os
import shutil
from collections import defaultdict

import gnupg
from apps.split_logs.models import Course
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
from apps.split_logs.utils import dump_course
from apps.split_logs.utils import s3_upload_file
from apps.split_logs.utils import SplitLogsUtilsDumpCourseException
from apps.split_logs.utils import SplitLogsUtilsUploadFileException
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from openedx_course_structure import course_structure


class CourseXmlDumpException(Exception):
    """Base class for other exceptions"""
    pass


class Command(SMSCommand):
    help = "Course XML dump, save it to S3, extract course structure"

    def add_arguments(self, parser):
        parser.add_argument('--org', type=str, required=True)
        parser.add_argument('--course_id', type=str)

    def handle(self, *args, **options):
        self.setOptions(**options)

        self.org = options['org']
        self._prepare_organisation()
        self._create_destination_dir()

        self._info(f"organisation: {self.organisation.name}")

        if options['course_id']:
            self._process_course(options['course_id'])
        else:
            self._process_organisation()

    def _prepare_organisation(self) -> None:
        try:
            self.organisation = Organisation.objects.get(
                active=True,
                name=self.org,
            )
            self.destination_dir = self._dump_dir()
        except ObjectDoesNotExist:
            raise CourseXmlDumpException(
                f"Organisation {self.org=} doesn't exist"
            )

    def _process_organisation(self):
        ok, ko = [], []
        for course_id in self._get_courses():
            if self._process_course(course_id):
                ok.append(course_id)
            else:
                ko.append(course_id)

        self._send_email(ok, ko)

    def _process_course(self, course_id: str) -> bool:
        self._info(f"course: {course_id}")
        try:
            course_file = dump_course(
                self.organisation,
                course_id,
                self.destination_dir
            )
            self._update_course_structure(course_id, course_file)
            if self.organisation.public_key:
                course_file_encrypted = self._encrypt(course_file)
                self._upload(course_file_encrypted)
            else:
                self._upload(course_file)
        except SplitLogsUtilsDumpCourseException as error:
            self._error(f"dump course {error=}")
            return False
        except SplitLogsUtilsUploadFileException as error:
            self._error(f"upload course {error=}")
            return False
        except CourseXmlDumpException as error:
            self._error(f"script exception: <{error}>")
            return False

        return True

    def _update_course_structure(self, course_id, course_file):
        try:
            course = Course.objects.get(
                organisation=self.organisation,
                course_id=course_id
            )
            course.structure = course_structure.structure(course_file)
            course.save()
        except course_structure.OpenEdxCourseStructureException as error:
            raise CourseXmlDumpException(
                f"Course {course_id=} structure exception {error=}"
            )
        except ObjectDoesNotExist:
            raise CourseXmlDumpException(
                f"Course {course_id=} doesn't exist"
            )

    def _upload(self, fname):
        s3_upload_file(
            self.organisation.bucket_name,
            self.organisation,
            fname,
            "{org}/dump-xml/{date}/{name}".format(
                org=self.organisation.name,
                date=fname.split("/")[-2],
                name=os.path.basename(fname)
            )
        )

    def _encrypt(self, fname):
        gpg = gnupg.GPG()
        gpg.encoding = "utf-8"
        gpg.import_keys(self.organisation.public_key.value)
        fname_encrypted = "{}.gpg".format(fname)
        with open(fname, "rb") as f:
            status = gpg.encrypt_file(
                f,
                armor=True,
                recipients=[self.organisation.public_key.recipient],
                output=fname_encrypted,
            )
            if status.ok:
                os.remove(fname)
            else:
                raise CourseXmlDumpException("Encrypt file error")
        return fname_encrypted

    def _dump_dir(self):
        return "{}/{}".format(
            self._organisation_dir(),
            self.now
        )

    def _structure_dir(self):
        return "{}/{}".format(
            self._organisation_dir(),
            'structure'
        )

    def _organisation_dir(self):
        return "{}/{}".format(
            settings.DUMP_XML_PATH,
            self.organisation.name.lower(),
        )

    def _create_destination_dir(self):
        try:
            shutil.rmtree(self.destination_dir)
        except FileNotFoundError:
            pass

        # create directory
        os.makedirs(self.destination_dir)

    def _send_email(self, ok, ko):
        nok = len(ok)
        nko = len(ko)
        result_message = []
        result_message.append(f"{nok} courses were dumped out of {nok + nko}")
        if nko > 0:
            result_message.append("There are errors in the courses below:")
            for course in ko:
                result_message.append(f"{course}")

        result_message.append("")
        result_message.append("Detailed log:")

        self.message = result_message + self.message

        self.send_email(f"Course XML dump {self.organisation.name}")

    def _get_courses(self):
        cursor = self.edxapp_cursor()
        cursor.execute(
            "SELECT course_id FROM {db_name}.student_courseenrollment GROUP BY course_id".format(
                db_name=f"docker_{self.organisation.name.lower()}_edxapp"
            )
        )
        return map(lambda v: v[0], cursor.fetchall())
