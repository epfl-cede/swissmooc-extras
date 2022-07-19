# -*- coding: utf-8 -*-
import datetime
import os
import sys

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from migrate.deleteCourse import DeleteCourse
from migrate.helpers import APP_ENVS
from migrate.helpers import DESTINATIONS

class Command(BaseCommand):
    help = 'Delete particular course and related student activity'

    def add_arguments(self, parser):
        parser.add_argument('--destination', help='Destination DB', nargs='?', type=str, required=True)
        parser.add_argument('--course_id', help='course_id', required=True)
        parser.add_argument('--debug', action='store_true', help='Debug info')

    def handle(self, *args, **options):
        APP_ENV = os.getenv('SMS_APP_ENV')
        if APP_ENV not in APP_ENVS:
            raise CommandError('Please, provide app environment(staging|campus)')
        if options['destination'] not in DESTINATIONS[APP_ENV]:
            raise CommandError('Destination "%s" not in the list' % options['destination'])

        Delete = DeleteCourse(
            APP_ENV,
            options['destination'],
            options['course_id'],
            options['debug']
        )
        Delete.run()
