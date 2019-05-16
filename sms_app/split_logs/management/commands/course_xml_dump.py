import os, stat
import json
import shutil
import datetime
import logging
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Course XML dump; running on one of the app server during the night'

    def handle(self, *args, **options):
        now = datetime.datetime.now().date()
        cdir = '{}/{}/'.format(settings.DUMP_XML_PATH, now)

        # remove dir and all contents
        try:
            shutil.rmtree(cdir)
        except FileNotFoundError:
            pass

        # create directory
        os.mkdir(cdir)
        os.chmod(cdir, 0o777);

        # get list of courses
        cmd = [
            'sudo',
            '-u',
            'www-data',
            '/edx/bin/python.edxapp',
            '/edx/bin/manage.edxapp',
            'lms',
            'dump_course_ids',
            '--settings',
            'openstack',
        ]
        subprocess.run(cmd, shell=False, check=True, stdout=subprocess.PIPE)
        output = proc.stdout.read()
        #output = ['course-v1:BFH+MATLAB+2018', 'course-v1:CSM+0.5+2018']
        for course_id in output:
            course_dir = '{}/{}/'.format(cdir, course_id[10:].replace('+', '-'))
            os.mkdir(course_dir)
            os.chmod(course_dir, 0o777);

            # dump course
            cmd = [
                'sudo',
                '-u',
                'www-data',
                '/edx/bin/python.edxapp',
                '/edx/bin/manage.edxapp',
                'cms',
                'export',
                '--settings',
                'openstack',
                course_id,
            ]
            subprocess.run(cmd, shell=False, check=True)

            # zip course
            zip_name = shutil.make_archive(course_dir, 'zip', os.path.dirname(course_dir), os.path.basename(course_dir))
            
            # sync course
            cmd  = [
                'rsync',
                '-avz',
                '--delete',
                os.path.dirname(zip_name),
                'ubuntu@192.168.{}.191:{}/'.format(settings.EDXAPP_MYSQL_HOST.split('.')[2], settings.DUMP_XML_PATH)
            ]
            subprocess.run(cmd, shell=False, check=True)
            
            # remove course
            shutil.rmtree(course_folder)
            shutil.rmtree('{}.zip'.format(course_folder))
