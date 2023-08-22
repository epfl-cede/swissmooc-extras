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

    def handle_verbosity(self, options):
        verbosity = int(options["verbosity"])
        self._handle_verbosity('split_logs', verbosity)
        self._handle_verbosity('check_ssl', verbosity)

    def _handle_verbosity(self, app, verbosity):
        logger = logging.getLogger(app)

        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        elif verbosity > 0:
            logger.setLevel(logging.INFO)

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

    def debug(self, message):
        self.logger.debug(message)
        now = datetime.datetime.now()
        self.message.append(f"[{now:%Y-%m-%d %H:%M}] DEBUG {message}")

    def info(self, message):
        self.logger.info(message)
        now = datetime.datetime.now()
        self.message.append(f"[{now:%Y-%m-%d %H:%M}] INFO {message}")

    def warning(self, message):
        self.logger.warning(message)
        now = datetime.datetime.now()
        self.message.append(f"[{now:%Y-%m-%d %H:%M}] WARNING {message}")

    def error(self, message):
        self.is_error = True
        self.logger.error(message)
        now = datetime.datetime.now()
        self.message.append(f"[{now:%Y-%m-%d %H:%M}] ERROR {message}")
