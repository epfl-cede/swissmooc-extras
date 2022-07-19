# -*- coding: utf-8 -*-
import logging
import os

import gnupg
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import connections
from split_logs.models import ACTIVE
from split_logs.models import Course
from split_logs.models import CourseDump
from split_logs.models import NO
from split_logs.models import NOT_ACTIVE
from split_logs.models import Organisation
from split_logs.models import YES

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Course DB encrypt files'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=3)

    def handle(self, *args, **options):
        limit = options['limit']
        cnt = 0
        org_processed = {}

        gpg = gnupg.GPG()
        gpg.encoding = 'utf-8'
        files = CourseDump.objects.filter(is_encypted=NO)
        for cd in files:
            logger.info("encrypt file for course %s table %s", cd.course.name, cd.table.name)

            if cd.course.organisation.name not in org_processed:
                importres = gpg.import_keys(cd.course.organisation.public_key.value)
                gpg.trust_keys(importres.fingerprints, 'TRUST_ULTIMATE')
                org_processed[cd.course.organisation.name] = True

            with open(cd.dump_file_name(), 'rb') as f:
                status = gpg.encrypt_file(
                    f,
                    armor=True,
                    recipients=[cd.course.organisation.public_key.recipient],
                    output=cd.encrypred_file_name()
                )
                if status.ok:
                    logger.info("OK")
                    os.remove(cd.dump_file_name())
                    cd.is_encypted = YES
                    cd.save()
                else:
                    logger.error("ERROR: %s", status.status)
