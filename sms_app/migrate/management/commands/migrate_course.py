import os
import sys
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from migrate.migrateUser import MigrateUser
from migrate.migrateCourse import MigrateCourse
from migrate.helpers import APP_ENVS, DESTINATIONS

class Command(BaseCommand):
    help = 'Migrate particular course'
    modes = [
        'course',
        'users',
        'full'
    ]

    def add_arguments(self, parser):
        parser.add_argument('--destination', help='Destination DB', nargs='?', type=str, required=True)
        parser.add_argument('--course_id', help='course_id', required=True)
        parser.add_argument('--mode', help='mode', required=True)
        parser.add_argument('--overwrite', action='store_true', help='Overwrite existing data')
        parser.add_argument('--staff_only', action='store_true', help='Migrate staff users only')
        parser.add_argument('--ignore_user_migration', action='store_true', default=False, help='Do not exit if user can\'t be migrated')
        parser.add_argument('--debug', action='store_true', help='Debug info')
        parser.set_defaults(users_only=False)
        parser.set_defaults(overwrite=False)

    def handle(self, *args, **options):
        APP_ENV = os.getenv('SMS_APP_ENV')
        if APP_ENV not in APP_ENVS:
            raise CommandError('Please, provide app environment(staging|campus)')
        if options['destination'] not in DESTINATIONS[APP_ENV]:
            raise CommandError('Destination "%s" not in the list' % options['destination'])
        if options['mode'] not in self.modes:
            raise CommandError('Mode "%s" not in the list' % options['mode'])

        Migrate = MigrateCourse(
            APP_ENV,
            options['destination'],
            options['course_id'],
            options['overwrite'],
            options['ignore_user_migration'],
            options['debug']
        )
        if Migrate.check_users():
            if options['mode'] == 'course':
                Migrate.run_course()
            elif options['mode'] == 'users':
                Migrate.run_users()
            else:
                Migrate.run_full()
