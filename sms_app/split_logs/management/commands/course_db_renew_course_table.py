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

        for organisation in Organisation.objects.filter(active=True):
            self.info(f"process organization {organisation.name}")
            Course.objects.filter(organisation=organisation).update(active=NOT_ACTIVE)

            cursor = self.edxapp_cursor()
            cursor.execute(
                "SELECT course_id FROM {db_name}.student_courseenrollment GROUP BY course_id".format(
                    db_name="docker_" + organisation.name.lower() + "_edxapp",
                )
            )
            for row in cursor.fetchall():
                name = row[0]
                try:
                    self.info(f"Set course {name} as active")
                    course = Course.objects.get(name=name, organisation=organisation)
                    course.active = ACTIVE
                    course.save()
                except ObjectDoesNotExist:
                    self.info(f"Insert new course <{name}>")
                    Course.objects.create(name=row[0], organisation=organisation, active=ACTIVE)
