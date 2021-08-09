import sys
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from migrate.migrateUser import MigrateUser
from migrate.helpers import DESTINATIONS

class Command(BaseCommand):
    help = 'Migrate particular user'

    def add_arguments(self, parser):
        parser.add_argument('--destination', help='Destination DB', nargs='?', type=str, required=True)
        parser.add_argument('--user_id', help='user_id', required=True)
        parser.add_argument('--overwrite', action='store_true', help='Overwrite existing data')
        parser.add_argument('--debug', action='store_true', help='Debug info')
        parser.set_defaults(overwrite=False)

    def handle(self, *args, **options):
        if options['destination'] not in DESTINATIONS:
            raise CommandError('Destination "%s" not in the list' % options['destination'])

        Migrate = MigrateUser(
            options['destination'],
            options['user_id'],
            options['overwrite'],
            options['debug']
        )
        Migrate.run()
