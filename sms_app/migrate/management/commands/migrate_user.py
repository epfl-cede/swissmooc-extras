import sys
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from migrate.models_hawthorn import AuthUser

class Command(BaseCommand):
    help = 'Migrate particular user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='+', type=int)

    def handle(self, *args, **options):
        User = AuthUser.objects.using('edxapp_readonly').get(pk=options['user_id'])
