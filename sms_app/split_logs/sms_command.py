# -*- coding: utf-8 -*-
import datetime
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

class SMSCommand(BaseCommand):
    message = []
    now = datetime.datetime.now().date()
    is_error = False

    def handle_verbosity(self, options):
        verbosity = int(options["verbosity"])
        logger = logging.getLogger("split_logs")

        if verbosity > 1:
            logger.setLevel(logging.DEBUG)
        elif verbosity > 0:
            logger.setLevel(logging.INFO)

    def send_email(self, subject):
        send_mail(
            f"[SMS-extras:{settings.SMS_APP_ENV}] - {subject} - {'OK' if self.is_error == False else 'ERROR'} - {self.now}",
            "\n".join(self.message),
            settings.EMAIL_FROM_ADDRESS,
            #settings.EMAIL_TO_ADDRESSES,
            ('oleg.demakov@epfl.ch',),
            fail_silently=False,
        )

    def info(self, message):
        self.logger.info(message)
        now = datetime.datetime.now()
        self.message.append(f"[{now:%Y-%m-%d %H:%M}] INFO {message}")

    def error(self, message):
        self.is_error = True
        self.logger.error(message)
        now = datetime.datetime.now()
        self.message.append(f"[{now:%Y-%m-%d %H:%M}] ERROR {message}")
