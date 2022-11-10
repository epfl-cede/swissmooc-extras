# -*- coding: utf-8 -*-
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from split_logs.models import ACTIVE
from split_logs.models import Course
from split_logs.models import NOT_ACTIVE
from split_logs.models import Organisation
from split_logs.sms_command import SMSCommand


class Command(SMSCommand):
    help = "Renew table Course: remove outdated courses and add new"
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        self.handle_verbosity(options)

        organisations = Organisation.objects.filter(active=True)
        for o in organisations:
            self.info(f"process organization {o.name}")
            Course.objects.filter(organisation=o).update(active=NOT_ACTIVE)

            cursor = self.edxapp_cursor()
            cursor.execute("SELECT course_id FROM student_courseenrollment GROUP BY course_id")
            for row in cursor.fetchall():
                name = row[0]
                try:
                    self.info(f"Set course {name} as active")
                    course = Course.objects.get(name=name, organisation=o)
                    course.active = ACTIVE
                    course.save()
                except ObjectDoesNotExist:
                    self.info(f"Insert new course <{name}>")
                    Course.objects.create(name=row[0], organisation=o, active=ACTIVE)
