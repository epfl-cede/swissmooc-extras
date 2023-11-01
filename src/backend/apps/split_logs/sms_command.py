# -*- coding: utf-8 -*-
import datetime
import logging

import MySQLdb
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

class SMSCommand(BaseCommand):
    message = []
    now = datetime.datetime.now().date()
    is_error = False

    def setOptions(self, **options):
        if "verbosity" in options:
            verbosity = int(options["verbosity"])
            root_logger = logging.getLogger("")
            if verbosity == 3:
                root_logger.setLevel(logging.DEBUG)
            elif verbosity == 2:
                root_logger.setLevel(logging.INFO)
            else:
                root_logger.setLevel(logging.WARNING)


    def edxapp_cursor(self):
        db = MySQLdb.connect(**settings.EDXAPP_DATABASES['readonly'])
        return db.cursor()

    def send_email(self, subject):
        send_mail(
            f"[SMS-extras/{settings.SMS_APP_ENV}] - {subject} - {'OK' if self.is_error == False else 'ERROR'} - {self.now}",
            "\n".join(self.message),
            settings.EMAIL_FROM_ADDRESS,
            #settings.EMAIL_TO_ADDRESSES,
            ('oleg.demakov@epfl.ch',),
            fail_silently=False,
        )
