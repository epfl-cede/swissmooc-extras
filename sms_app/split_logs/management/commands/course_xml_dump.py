import os
import shutil
import datetime
import logging
import subprocess

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

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
        courses = self._get_courses()
        course_data_for_email = ()
        for course_id in courses:
            logger.info('process course_id %s', course_id)
            course_dir = '{}{}/'.format(cdir, course_id[10:].replace('+', '-'))
            os.mkdir(course_dir)
            os.chmod(course_dir, 0o777);

            result = self._course_dump(course_id, course_dir)
            course_data_for_email += (course_id, result)

            zip_name = self._course_zip(course_id, course_dir)
            self._course_copy(course_id, zip_name)
            
            # remove course
            os.remove(zip_name)

        self._send_email(course_data_for_email, now)

    def _send_email(self, r, now):
        list_failed = []
        list_success = []
        for c in r:
            if c[1] == True:
                list_success.append(c[0])
            else:
                list_failed.append(c[0])

        send_mail(
            'SMS-extras course_xml_dump result {}'.format(now),
            'Course XML dump results for {}:\n\nDUMP WITH ERROR COURSES:\n{}\n\nCOURSES WITHOUT PROBLEMS:\n{}'.format(
                now,
                '\n'.join(list_failed),
                '\n'.join(list_success),
            ),
            'noreply@epfl.ch',
            ['oleg.demakov@epfl.ch'],
            fail_silently=False,
        )

    def _course_copy(self, course_id, zip_name):
        cmd  = [
            'rsync',
            '-az',
            os.path.dirname(zip_name),
            'ubuntu@192.168.{}.191:{}/'.format(settings.EDXAPP_MYSQL_HOST.split('.')[2], settings.DUMP_XML_PATH)
        ]
        try:
            with open(os.devnull, 'w') as devnull:
                subprocess.run(cmd, shell=False, check=True, stderr=devnull, stdout=devnull)
        except Exception as e:
            logger.error('rsync course %s error: %s', course_id, e)
            exit(1)
        
    def _course_zip(self, course_id, course_dir):
        zip_name = shutil.make_archive(course_dir, 'zip', os.path.dirname(os.path.dirname(course_dir)), os.path.basename(course_dir[:-1]))
        shutil.rmtree(course_dir)
        return zip_name
        
    def _course_dump(self, course_id, course_dir):
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
            course_dir,
        ]
        result = True
        try:
            with open(os.devnull, 'w') as devnull:
                subprocess.run(cmd, shell=False, check=True, stderr=devnull, stdout=devnull)
        except Exception as e:
            logger.error('dump course %s error: %s', course_id, e)
            result = False

        subprocess.run(['sudo', 'chown', '-R', 'ubuntu:ubuntu', course_dir])
        return result
            
    def _get_courses(self):
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
        try:
            with open(os.devnull, 'w') as devnull:
                output = subprocess.check_output(cmd, stderr=devnull)
        except Exception as e:
            logger.error('get course list error: %s', e)
            exit(1)

        return output.decode().strip('\n').split('\n')
