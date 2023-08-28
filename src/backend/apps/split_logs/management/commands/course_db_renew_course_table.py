# -*- coding: utf-8 -*-
import logging

from apps.split_logs.models import Course
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections


class Command(SMSCommand):
    help = "Renew table Course: remove outdated courses and add new"
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.handle_verbosity(options)

        for organisation in Organisation.objects.filter(active=True):
            self.info(f"process organization {organisation.name}")
            Course.objects.filter(organisation=organisation).update(active=False)

            cursor = self.edxapp_cursor()
            cursor.execute(
                "SELECT course_id FROM {db_name}.student_courseenrollment GROUP BY course_id".format(
                    db_name="docker_" + organisation.name.lower() + "_edxapp",
                )
            )
            for row in cursor.fetchall():
                course_id = row[0]
                try:
                    self.info(f"Set course {course_id=} as active")
                    course = Course.objects.get(
                        course_id=course_id,
                        organisation=organisation
                    )
                    course.active = True
                    course.save()
                except ObjectDoesNotExist:
                    self.info(f"Insert new course <{course_id}>")
                    Course.objects.create(
                        course_id=row[0],
                        organisation=organisation,
                        active=True
                    )
