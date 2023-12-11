# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import MySQLdb
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class SMSCommand(BaseCommand):
    message = []
    now = datetime.now().date()
    is_error: bool = False
    is_warning: bool = False

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
        if self.is_error:
            status = 'ERROR'
        elif self.is_warning:
            status = 'WARNING'
        else:
            status = 'OK'

        send_mail(
            f"[SMS-extras/{settings.SMS_APP_ENV}] - {subject} - {status} - {self.now}",
            "\n".join(self.message),
            settings.EMAIL_FROM_ADDRESS,
            # settings.EMAIL_TO_ADDRESSES,
            ('oleg.demakov@epfl.ch',),
            fail_silently=False,
        )

    def _debug(self, message):
        logger.debug(message)
        self._message(message, 'DEBUG')

    def _info(self, message):
        logger.info(message)
        self._message(message, 'INFO')

    def _warning(self, message):
        self.is_warning = True
        logger.warning(message)
        self._message(message, 'WARNING')

    def _error(self, message):
        self.is_error = True
        logger.error(message)
        self._message(message, 'ERROR')

    def _message(self, message, level):
        now = datetime.now()
        self.message.append(f"[{now:%Y-%m-%d %H:%M}] {level} {message}")
