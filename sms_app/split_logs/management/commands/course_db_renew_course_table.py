import logging

from django.db import connections
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from split_logs.models import Course, Organisation, ACTIVE, NOT_ACTIVE

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Renew table Course: remove outdated courses and add new'

    def handle(self, *args, **options):
        organisations = Organisation.objects.filter(active=True)
        for o in organisations:
            logger.info("process organization %s", o.name)
            Course.objects.filter(organisation=o).update(active=NOT_ACTIVE)

            # find all courses belongs to organization in edx
            with connections['edxapp_readonly'].cursor() as cursor:
                cursor.execute("SELECT course_id FROM student_courseenrollment WHERE course_id LIKE %s GROUP BY course_id", ["%"+o.name+'%'])
                for row in cursor.fetchall():
                    name = row[0]
                    try:
                        logger.info("Set course %s as active", name)
                        course = Course.objects.get(name=name, organisation=o)
                        course.active = ACTIVE
                        course.save()
                    except ObjectDoesNotExist:
                        logger.info("Insert new course %s", name)
                        Course.objects.create(name=row[0], organisation=o, active=ACTIVE)
