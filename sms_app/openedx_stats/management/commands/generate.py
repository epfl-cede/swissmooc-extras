# -*- coding: utf-8 -*-
import csv
import datetime
import logging
import os
import pathlib
import re

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate basic stats from DB'

    database = ''
    course_id = None

    def handle(self, *args, **options):
        for self.database in settings.DATABASES:
            # skip default, id and old databases
            if self.database in ['default', 'edxapp_id', 'edxapp_readonly']: continue
            with connections[self.database].cursor() as cursor:
                print(' ===> process {}'.format(self.database))
                # get course_id
                for self.course_id in self.get_course_ids(cursor):
                    self.student_enrolments_by_date(cursor)
                    self.student_enrolments_by_mode(cursor)

    def student_enrolments_by_date(self, cursor):
        enrollments = self.get_enrolments_by_date(cursor)
        filename = '{}/{}/{}/{}.csv'.format(
            settings.STATS_FILE_PATH,
            self.database.split('_')[1],
            'student_enrolments_by_date',
            self.course_id
        )
        pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for r in enrollments:
                writer.writerow(r)

    def student_enrolments_by_mode(self, cursor):
        enrollments = self.get_enrolments_by_mode(cursor)
        filename = '{}/{}/{}/{}.csv'.format(
            settings.STATS_FILE_PATH,
            self.database.split('_')[1],
            'student_enrolments_by_mode',
            self.course_id
        )
        pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for r in enrollments:
                writer.writerow(r)

    def get_course_ids(self, cursor):
        cursor.execute("select DISTINCT course_id from student_courseenrollment")
        return [row[0] for row in cursor.fetchall()]

    def get_enrolments_by_date(self, cursor):
        cursor.execute("select date(created),count(*) from student_courseenrollment where course_id=%s GROUP BY 1", [self.course_id])
        return cursor.fetchall()

    def get_enrolments_by_mode(self, cursor):
        cursor.execute("select mode,count(*) from student_courseenrollment where course_id=%s GROUP BY 1", [self.course_id])
        return cursor.fetchall()
