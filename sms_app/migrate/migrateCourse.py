import logging
from datetime import datetime

from django.db import connections
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from migrate.models_hawthorn import (
    AuthUser,
    AuthUserProfile,
    AuthRegistration,
    StudentUserattribute,
    UserApiUserpreference,
)
from migrate.helpers import insertOrUpdateRow, selectRows
from migrate.migrateUser import MigrateUser

logger = logging.getLogger(__name__)

class MigrateCourse:
    def __init__(self, course_id, overwrite, debug):
        self.course_id = course_id
        self.overwrite = overwrite
        self.debug = debug

    def run(self):
        users =  selectRows('student_courseenrollment', {'course_id': self.course_id}, 'edxapp_readonly')
        if not users:
            logger.info("There isn't users in the course with id={}, are you sure you want to migrate this course?".format(self.course_id))
            exit(0)

        self.writeUsers(users)

    def writeUsers(self, users):
        for user in users:
            Migrate = MigrateUser(user['user_id'], self.overwrite, self.debug)
            Migrate.run()
