import logging

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

logger = logging.getLogger(__name__)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class MigrateUser:
    def __init__(self, user_id, overwrite, debug):
        self.user_id = user_id
        self.overwrite = overwrite
        self.debug = debug

    def run(self):
        data = self.getData()
        if data: self.writeData(data)

    def getData(self):
        result = {}
        User = self._fetchDataFromDB('auth_user', {'id': self.user_id}, 'edxapp_readonly')
        if not User:
            logger.info("User with id={} not find".format(self.user_id))
            exit(0)
        result['User'] = User[0]

        # relation: OneToOneField
        UserProfile =  self._fetchDataFromDB('auth_userprofile', {'user_id': self.user_id}, 'edxapp_readonly')
        result['UserProfile'] = UserProfile[0]

        # relation: OneToOneField
        Registration = self._fetchDataFromDB('auth_registration', {'user_id': self.user_id}, 'edxapp_readonly')
        result['Registration'] = Registration[0]

        # relation: ForeignKey
        Userattribute = self._fetchDataFromDB('student_userattribute', {'user_id': self.user_id}, 'edxapp_readonly')
        result['Userattribute'] = Userattribute

        # relation: ForeignKey
        ApiUserpreference = self._fetchDataFromDB('user_api_userpreference', {'user_id': self.user_id}, 'edxapp_readonly')
        result['ApiUserpreference'] = ApiUserpreference

        return result

    def _fetchDataFromDB(self, table_name, params, use):
        #User = AuthUser.objects.using('edxapp_readonly').get(pk=self.user_id)
        with connections[use].cursor() as cursor:
            cursor.execute(
                "SELECT * FROM {} WHERE {}".format(
                    table_name, " AND ".join(["{}=%s"]*len(params)).format(*params.keys())
                ),
                params.values()
            )
            return dictfetchall(cursor)
        
    def writeData(self, data):
        #print(data)
        if data['User']:
            self.writeDataId(data)
            #self.writeDataInstance(data)

    def writeDataId(self, data):
        # check user exists
        use = 'edxapp_id'
        User = self._getUser(data['User'], use)
        if User:
            if self.overwrite:
                print('User {} <{}> exists in destination DB, overwrite'.format(data['User']['username'], data['User']['email']))
                pk = self._insertOrUpdateUser(data['User'], use)
                self._insertOrUpdateUserProfile(pk, data['UserProfile'], use)
            else:
                print('User {} <{}> exists in destination DB, skip update, specify --overwrite to force update'.format(data['User']['username'], data['User']['email']))
        else:
            print('Add new user'.format(data['User']['username'], data['User']['email']))
            pk = self._insertOrUpdateUser(data['User'], use)
            self._insertOrUpdateUserProfile(pk, data['UserProfile'], use)


    def writeDataInstance(self, data):
        # check user exists
        #User = self._getUser(data['User'], 'edxapp_university')
        pass

    def _getUser(self, User, use):
        with connections[use].cursor() as cursor:
            cursor.execute(
                "SELECT * FROM auth_user WHERE username = %s AND email = %s",
                [User['username'], User['email']]
            )
            UserReturn = cursor.fetchone()
            if UserReturn:
                return UserReturn
            else:
                self._exitIfUserHasOneUniqueKey(User, use, 'username')
                self._exitIfUserHasOneUniqueKey(User, use, 'email')


    def _exitIfUserHasOneUniqueKey(self, User, use, key):
        with connections[use].cursor() as cursor:
            cursor.execute(
                "SELECT * FROM auth_user WHERE {} = %s".format(key),
                [User[key]]
            )
            User = cursor.fetchone()
            if User:
                logger.error("User {} <{}> exists only with {}".format(key))
                exit(1)


    def _insertOrUpdateUser(self, User, use):
        '''
         CREATE TABLE `auth_user` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `password` varchar(128) NOT NULL,
          `last_login` datetime DEFAULT NULL,
          `is_superuser` tinyint(1) NOT NULL,
          `username` varchar(150) NOT NULL,
          `first_name` varchar(30) NOT NULL,
          `last_name` varchar(30) NOT NULL,
          `email` varchar(254) NOT NULL,
          `is_staff` tinyint(1) NOT NULL,
          `is_active` tinyint(1) NOT NULL,
          `date_joined` datetime NOT NULL,
          PRIMARY KEY (`id`),
          UNIQUE KEY `username` (`username`),
          UNIQUE KEY `email` (`email`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8
        '''
        return self._insertOrUpdate(
            User,
            'auth_user',
            ['last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'],
            ['username', 'email'],
            use
        )

    def _insertOrUpdateUserProfile(self, pk, UserProfile, use):
        '''
        CREATE TABLE `auth_userprofile` (
         `id` int(11) NOT NULL AUTO_INCREMENT,
         `name` varchar(255) NOT NULL,
         `meta` longtext NOT NULL,
         `courseware` varchar(255) NOT NULL,
         `language` varchar(255) NOT NULL,
         `location` varchar(255) NOT NULL,
         `year_of_birth` int(11) DEFAULT NULL,
         `gender` varchar(6) DEFAULT NULL,
         `level_of_education` varchar(6) DEFAULT NULL,
         `mailing_address` longtext,
         `city` longtext,
         `country` varchar(2) DEFAULT NULL,
         `goals` longtext,
         `allow_certificate` tinyint(1) NOT NULL,
         `bio` varchar(3000) DEFAULT NULL,
         `profile_image_uploaded_at` datetime(6) DEFAULT NULL,
         `user_id` int(11) NOT NULL,
         `phone_number` varchar(50) DEFAULT NULL,
         `state` varchar(2) DEFAULT NULL,
         PRIMARY KEY (`id`),
         UNIQUE KEY `user_id` (`user_id`),
         KEY `auth_userprofile_name_50909f10` (`name`),
         KEY `auth_userprofile_language_8948d814` (`language`),
         KEY `auth_userprofile_location_ca92e4f6` (`location`),
         KEY `auth_userprofile_year_of_birth_6559b9a5` (`year_of_birth`),
         KEY `auth_userprofile_gender_44a122fb` (`gender`),
         KEY `auth_userprofile_level_of_education_93927e04` (`level_of_education`),
         CONSTRAINT `auth_userprofile_user_id_62634b27_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1
        '''
        UserProfile['user_id'] = pk
        return self._insertOrUpdate(
            UserProfile,
            'auth_userprofile',
            ['name', 'meta', 'courseware', 'language', 'location', 'year_of_birth', 'gender', 'level_of_education', 'mailing_address', 'city', 'country', 'goals', 'allow_certificate', 'bio', 'profile_image_uploaded_at', 'user_id'],
            ['user_id'],
            use
        )

    def _insertOrUpdate(self, Object, table_name, fields, unique_keys, use):
        with connections[use].cursor() as cursor:
            fields_for_update = fields.copy()
            for f in unique_keys:
                fields_for_update.remove(f)

            values_for_update = []
            for f in fields:
                values_for_update.append(Object[f])
            for f in fields_for_update:
                values_for_update.append(Object[f])

            sql = "INSERT INTO {} ".format(table_name) + \
                "({}) VALUES ".format(",".join(fields)) + \
                "({}) ".format(", ".join(["%s"]*len(fields))) + \
                "ON DUPLICATE KEY UPDATE " + \
                (",".join(["{}=%s"]*len(fields_for_update))).format(*fields_for_update)

            if self.debug:
                logger.info("SQL={}".format(sql))
                logger.info("values={}".format(values_for_update))

            cursor.execute(sql, values_for_update)

            sql = "SELECT id FROM {} WHERE {}".format(
                table_name, " AND ".join(["{}=%s"]*len(unique_keys)).format(*unique_keys)
            )
            if self.debug:
                logger.info("SQL={}".format(sql))
                logger.info("values={}".format([Object[f] for f in unique_keys]))
            cursor.execute(
                sql,
                [Object[f] for f in unique_keys]
            )
            return cursor.fetchone()[0]
