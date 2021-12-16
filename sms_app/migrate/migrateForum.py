import re
import os
import logging
import json
from datetime import datetime
from pymongo import MongoClient, errors

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
from migrate.helpers import insertOrUpdateRow, selectRows, selectRowsIn, selectField, selectFieldIn, copyTable, cmd
from migrate.helpers import CONNECTION_SOURCE, CONNECTION_ID
from migrate.migrateUser import MigrateUser

COLLECTION_SOURCE = 'cs_comments_service'

logger = logging.getLogger(__name__)

class migrateForumException(BaseException):
    pass

class MigrateForum:
    def __init__(self, APP_ENV, destination, course_id, overwrite, debug):
        self.APP_ENV = APP_ENV
        self.destination = destination
        self.course_id = course_id
        self.overwrite = overwrite
        self.debug = debug

        self.db_src = self._connection(
            os.environ.get('MONGODB_USER_SRC', ''),
            os.environ.get('MONGODB_PASSWORD_SRC', ''),
            COLLECTION_SOURCE
        )
        self.db_dst = self._connection(
            os.environ.get('MONGODB_USER_DST', ''),
            os.environ.get('MONGODB_PASSWORD_DST', ''),
            "{}_cs_comments_service".format(destination)
        )

        self.user_id_map = {}

    def _connection(self, user, password, collection):
        client = MongoClient(
            'mongodb://%s:%s@%s/%s' % (
                user,
                password,
                os.environ.get('MONGODB_HOST', ''),
                collection
            ))
        return client[collection]

        
    def run(self):
        try:
            self.migrateForumUsers()
            self.migrateForumContents()
            self.migrateForumSubscriptions()
        except Exception as e:
            logger.error(e)
            raise e

    def _migrateUser(self, user_id):
        # mysql
        Migrate = MigrateUser(self.APP_ENV, self.destination, user_id, self.overwrite, self.debug, False)
        Migrate.run()

        # mongodb
        user = self.db_src.users.find_one({'external_id': user_id})
        user['external_id'] = str(Migrate.pk)
        user['_id'] = str(Migrate.pk)
        try:
            self.db_dst.users.insert(user)
        except errors.DuplicateKeyError:
            pass

        self.user_id_map[user_id] = str(Migrate.pk)

    def migrateForumUsers(self):
        # find all posts for the course
        users = {}
        for post in self.db_src.contents.find({'course_id': self.course_id}):
            users[post['author_username']] = str(post['author_id'])

        for user_name in users:
            user_id = users[user_name]
            self._migrateUser(user_id)

    def migrateForumContents(self):
        # contents: author_id, course_id
        for post in self.db_src.contents.find({'course_id': self.course_id}):
            post['author_id'] = self.user_id_map[post['author_id']]
            try:
                self.db_dst.contents.insert(post)
            except errors.DuplicateKeyError:
                pass

    def migrateForumSubscriptions(self):
        # subscriptions: subscriber_id, source_id?
        for subscription in self.db_src.subscriptions.find({'subscriber_id': {"$in": [user_id for user_id in self.user_id_map]}}):
            subscription['subscriber_id'] = self.user_id_map[subscription['subscriber_id']]
            try:
                self.db_dst.subscriptions.insert(subscription)
            except errors.DuplicateKeyError:
                pass

    def selectRows(self, table_name, select):
        return selectRows(
            table_name,
            select,
            CONNECTION_SOURCE,
            self.debug
        )

    def selectRowsIn(self, table_name, param, values):
        return selectRowsIn(
            table_name,
            param,
            values,
            CONNECTION_SOURCE,
            self.debug
        )

