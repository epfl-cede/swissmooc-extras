import os
import shutil
import datetime
import logging
import gnupg

from django.conf import settings
from django.core.management.base import BaseCommand

from split_logs.utils import upload_file
from split_logs.models import Organisation

LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Course XML dump; encrypt and upload course XMLs'

    def handle(self, *args, **options):
        organisations = Organisation.objects.all()

        now = datetime.datetime.now().date()
        dirs = [os.path.join(settings.DUMP_XML_PATH, o) for o in os.listdir(settings.DUMP_XML_PATH) if os.path.isdir(os.path.join(settings.DUMP_XML_PATH, o))]
        for cdir in dirs:
            LOGGER.info('Process dir for encrypt %s', cdir)
            files = [os.path.join(cdir, o) for o in os.listdir(cdir) if not os.path.isdir(os.path.join(cdir, o)) and o.endswith('.zip')]

            for cfile in files:
                LOGGER.info('Encrypt file %s', cfile)
                org = self._find_org_by_name(os.path.basename(cfile).split('-')[0])

                self._encrypt(org, cfile)

            LOGGER.info('Process dir for upload %s', cdir)
            files = [os.path.join(cdir, o) for o in os.listdir(cdir) if not os.path.isdir(os.path.join(cdir, o)) and o.endswith('.gpg')]

            for efile in files:
                LOGGER.info('Upload file %s', efile)
                org = self._find_org_by_name(os.path.basename(efile).split('-')[0])

                upload_file(org, efile, '{org}/dump-xml/{date}/{name}'.format(
                    org=org.name,
                    date=efile.split('/')[-2],
                    name=os.path.basename(efile)
                ))
                

    def _encrypt(self, org, fname):
        gpg = gnupg.GPG()
        gpg.encoding = 'utf-8'
        importres = gpg.import_keys(org.public_key.value)
        gpg.trust_keys(importres.fingerprints, 'TRUST_ULTIMATE')
        with open(fname, 'rb') as f:
            status = gpg.encrypt_file(
                f,
                armor=True,
                recipients=[org.public_key.recipient],
                output='{}.gpg'.format(fname),
            )
            if status.ok:
                LOGGER.info("OK")
                os.remove(fname)
            else:
                LOGGER.error("ERROR: %s", status.status)
                
    def _find_org_by_name(self, name):
        try:
            org = Organisation.objects.get(name=name);
        except Exception as e:
            print(e)
        return org
