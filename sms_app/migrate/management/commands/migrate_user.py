import os
import sys
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from migrate.migrateUser import MigrateUser
from migrate.helpers import APP_ENVS, DESTINATIONS

class Command(BaseCommand):
    help = 'Migrate particular user'

    def add_arguments(self, parser):
        parser.add_argument('--destination', help='Destination DB', nargs='?', type=str, required=True)
        parser.add_argument('--user_id', help='user_id', required=True)
        parser.add_argument('--overwrite', action='store_true', help='Overwrite existing data')
        parser.add_argument('--debug', action='store_true', help='Debug info')
        parser.set_defaults(execute=False)

    def handle(self, *args, **options):
        APP_ENV = os.getenv('SMS_APP_ENV')
        if APP_ENV not in APP_ENVS:
            raise CommandError('Please, provide app environment(staging|campus)')
        if options['destination'] not in DESTINATIONS[APP_ENV]:
            raise CommandError('Destination "%s" not in the list' % options['destination'])

        Migrate = MigrateUser(
            APP_ENV,
            options['destination'],
            options['user_id'],
            options['overwrite'],
            options['debug']
        )
        Migrate.run()
