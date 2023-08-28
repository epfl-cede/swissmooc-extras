# -*- coding: utf-8 -*-
import logging
import os

import gnupg
from apps.split_logs.models import Course
from apps.split_logs.models import CourseDump
from apps.split_logs.models import Organisation
from apps.split_logs.sms_command import SMSCommand
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections


class Command(SMSCommand):
    help = "Course DB encrypt files"
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=3)

    def handle(self, *args, **options):
        self.handle_verbosity(options)

        # limit = options["limit"]
        cnt = 0
        org_processed = {}

        gpg = gnupg.GPG()
        gpg.encoding = "utf-8"
        files = CourseDump.objects.filter(is_encypted=False)
        for cd in files:
            self.info(f"encrypt file for course <{cd.course.name}> table <{cd.table.name}>")

            if cd.course.organisation.name not in org_processed:
                importres = gpg.import_keys(cd.course.organisation.public_key.value)
                org_processed[cd.course.organisation.name] = True

            with open(cd.dump_file_name(), "rb") as f:
                status = gpg.encrypt_file(
                    f,
                    armor=True,
                    recipients=[cd.course.organisation.public_key.recipient],
                    output=cd.encrypred_file_name()
                )
                if status.ok:
                    self.info("OK")
                    os.remove(cd.dump_file_name())
                    cd.is_encypted = True
                    cd.save()
                else:
                    self.error(f"Encrypt file error: <{status.status}>")
