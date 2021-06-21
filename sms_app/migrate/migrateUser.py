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

logger = logging.getLogger(__name__)

CONNECTION_ID = 'edxapp_id'
CONNECTION_UNIVERSITY = 'edxapp_university'

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

        Usersocialauth = self._fetchDataFromDB('social_auth_usersocialauth', {'user_id': self.user_id}, 'edxapp_readonly')
        if not Usersocialauth:
            logger.error("User {} <{}> doesn't have any social auth, exit'".format(User[0]['email'], User[0]['username']))
            exit(1)
        result['Usersocialauth'] = Usersocialauth

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
        if data['User']:
            self.writeAuthData(data, CONNECTION_ID)
            self.writeAuthData(data, CONNECTION_UNIVERSITY)

    def writeAuthData(self, data, connection):
        # check user exists
        # replace 966186222692@eduid.ch to 735531216246_eduid_ch
        # replace 240575@epfl.ch to 253705_epfl_ch
        data['User']['username'].replace('@', '_').replace('.', '_')
        User = self._getUser(data['User'], connection)
        if User:
            if self.overwrite:
                print('User {} <{}> exists in destination DB, overwrite'.format(data['User']['username'], data['User']['email']))
                pk = self._insertOrUpdateUser(data['User'], connection)
                self._insertOrUpdateUserProfile(pk, data['UserProfile'], connection)
                self._insertOrUpdateRegistration(pk, data['Registration'], connection)
                self._insertOrUpdateUserattribute(pk, data['Userattribute'], connection)
                self._insertOrUpdateApiUserpreference(pk, data['ApiUserpreference'], connection)
                self._insertOrUpdateUsersocialauth(pk, data['User']['username'], data['Usersocialauth'], connection)
            else:
                print('User {} <{}> exists in destination DB, skip update, specify --overwrite to force update'.format(data['User']['username'], data['User']['email']))
        else:
            print('Add new user'.format(data['User']['username'], data['User']['email']))
            pk = self._insertOrUpdateUser(data['User'], connection)
            self._insertOrUpdateUserProfile(pk, data['UserProfile'], connection)
            self._insertOrUpdateRegistration(pk, data['Registration'], connection)
            self._insertOrUpdateUserattribute(pk, data['Userattribute'], connection)
            self._insertOrUpdateApiUserpreference(pk, data['ApiUserpreference'], connection)
            self._insertOrUpdateUsersocialauth(pk, data['User']['username'], data['Usersocialauth'], connection)

    def _getUser(self, User, connection):
        with connections[connection].cursor() as cursor:
            cursor.execute(
                "SELECT * FROM auth_user WHERE username = %s AND email = %s",
                [User['username'], User['email']]
            )
            UserReturn = cursor.fetchone()
            if UserReturn:
                return UserReturn
            else:
                self._exitIfUserHasOneUniqueKey(User, connection, 'username')
                self._exitIfUserHasOneUniqueKey(User, connection, 'email')


    def _exitIfUserHasOneUniqueKey(self, User, connection, key):
        with connections[connection].cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM auth_user WHERE {} = %s".format(key),
                [User[key]]
            )
            UserCheck = cursor.fetchone()
            if UserCheck:
                logger.error("User {} <{}> exists only with '{}' on '{}'".format(User['email'], User['username'], key, connection))
                exit(1)


    def _insertOrUpdateUser(self, User, connection):
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
            connection
        )

    def _insertOrUpdateUserProfile(self, pk, UserProfile, connection):
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
        self._insertOrUpdate(
            UserProfile,
            'auth_userprofile',
            ['name', 'meta', 'courseware', 'language', 'location', 'year_of_birth', 'gender', 'level_of_education', 'mailing_address', 'city', 'country', 'goals', 'allow_certificate', 'bio', 'profile_image_uploaded_at', 'user_id'],
            ['user_id'],
            connection
        )

    def _insertOrUpdateRegistration(self, pk, Registration, connection):
        '''
        CREATE TABLE `auth_registration` (
         `id` int(11) NOT NULL AUTO_INCREMENT,
         `activation_key` varchar(32) NOT NULL,
         `user_id` int(11) NOT NULL,
         PRIMARY KEY (`id`),
         UNIQUE KEY `activation_key` (`activation_key`),
         UNIQUE KEY `user_id` (`user_id`),
         CONSTRAINT `auth_registration_user_id_f99bc297_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1
        '''
        Registration['user_id'] = pk
        self._insertOrUpdate(
            Registration,
            'auth_registration',
            ['activation_key', 'user_id'],
            ['user_id'],
            connection
        )

    def _insertOrUpdateUserattribute(self, pk, Userattribute, connection):
        '''
        CREATE TABLE `student_userattribute` (
         `id` int(11) NOT NULL AUTO_INCREMENT,
         `created` datetime(6) NOT NULL,
         `modified` datetime(6) NOT NULL,
         `name` varchar(255) NOT NULL,
         `value` varchar(255) NOT NULL,
         `user_id` int(11) NOT NULL,
         PRIMARY KEY (`id`),
         UNIQUE KEY `student_userattribute_user_id_name_70e18f46_uniq` (`user_id`,`name`),
         KEY `student_userattribute_name_a55155e3` (`name`),
         CONSTRAINT `student_userattribute_user_id_19c01f5e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1
        '''
        for ua in Userattribute:
            ua['user_id'] = pk
            self._insertOrUpdate(
                ua,
                'student_userattribute',
                ['created', 'modified', 'name', 'value', 'user_id'],
                ['user_id'],
                connection
            )

    def _insertOrUpdateApiUserpreference(self, pk, ApiUserpreference, connection):
        '''
        CREATE TABLE `user_api_userpreference` (
         `id` int(11) NOT NULL AUTO_INCREMENT,
         `key` varchar(255) NOT NULL,
         `value` longtext NOT NULL,
         `user_id` int(11) NOT NULL,
         PRIMARY KEY (`id`),
         UNIQUE KEY `user_api_userpreference_user_id_key_17924c0d_uniq` (`user_id`,`key`),
         KEY `user_api_userpreference_key_9c8a8f6b` (`key`),
         CONSTRAINT `user_api_userpreference_user_id_68f8a34b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1
        '''
        for ua in ApiUserpreference:
            ua['user_id'] = pk
            self._insertOrUpdate(
                ua,
                'user_api_userpreference',
                ['key', 'value', 'user_id'],
                ['user_id'],
                connection
            )

    def _insertOrUpdateUsersocialauth(self, pk, username, Usersocialauth, connection):
        '''
        CREATE TABLE `social_auth_usersocialauth` (
         `id` int(11) NOT NULL AUTO_INCREMENT,
         `provider` varchar(32) NOT NULL,
         `uid` varchar(255) NOT NULL,
         `extra_data` longtext NOT NULL,
         `user_id` int(11) NOT NULL,
         `created` datetime(6) NOT NULL,
         `modified` datetime(6) NOT NULL,
         PRIMARY KEY (`id`),
         UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
         KEY `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` (`user_id`),
         KEY `social_auth_usersocialauth_uid_796e51dc` (`uid`),
         CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin
        '''
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for ua in Usersocialauth:
            uid = self._translateUid(ua['uid'])
            if uid:
                if connection == CONNECTION_ID:
                    self._insertOrUpdate(
                        {
                            'provider': ua['provider'],
                            'uid': uid,
                            'extra_data': ua['extra_data'],
                            'user_id': pk,
                            'created': now,
                            'modified': now,
                        },
                        'social_auth_usersocialauth',
                        ['provider', 'uid', 'extra_data', 'user_id', 'created', 'modified'],
                        ['user_id'],
                        connection
                    )
                else:
                    self._insertOrUpdate(
                        {
                            'provider': 'edx-oauth2',
                            # remove first part from string like 'switch-edu-id:735531216246_eduid_ch'
                            'uid': username,
                            'extra_data': '{}',
                            'user_id': pk,
                            'created': now,
                            'modified': now,
                        },
                        'social_auth_usersocialauth',
                        ['provider', 'uid', 'extra_data', 'user_id', 'created', 'modified'],
                        ['user_id'],
                        connection
                    )
                    # only one connection is needed
                    break

    def _translateUid(self, uid):
        # translate 5e5ca030c983ab469dc3f6249ae239:258585@epfl.ch to epfl:258585@epfl.ch
        # translate e555442cd67c9e3ae0436f5b506d6c:714597953495@eduid.ch to switch-edu-id:735531216246@eduid.ch
        # get this values from https://courses.swissmooc.ch/admin/third_party_auth/samlproviderconfig/?q=idp.epfl.ch
        providers_map = {
            'switch-edu-id': [
                # staging
                'e555442cd67c9e3ae0436f5b506d6c',
                '719e3c350a1927223be1723d4a5ed0',
                # campus
                '0afa10bd0b43cc80f209d31e6b2ce2',
                '2e89408363c69f1b2393ff0d75ffd0',
                '6f354848093935d0d00e3735319ee2',
                '7975f3db9039ea5266e44ed4569907',
                'a0ddec20e7fe8ee2d6a82d4041b9b3',
                'b1150456ac6d78d77f2d7bc3b0ae5a',
                'b3850434bb2f87e9e7277c0fa87ce9',
                'bcd434f32188265c353c0b3a2d2af7',
                'c788487ec165538e07bf0cc846f7c4',
                'c94c3dce582c816a4f8ce482f5b11f',
                'd1b7c62067ae0d324af91f417bb982',
                'db9ccf5b1390af0bd62b843099befb',
            ],
            'epfl': [
                # staging
                '5e5ca030c983ab469dc3f6249ae239',
                # campus
                'eff426fd0f4172d33a7073de4501f0',
                '3c89411445a104c9a973b8a088cb83',
                '5e5ca030c983ab469dc3f6249ae239',
            ],
        }
        for provider_map in providers_map:
            for provider_uid in providers_map[provider_map]:
                if uid.find(provider_uid) == 0:
                    uid = uid.replace(provider_uid, provider_map)
                    return uid
        return False
        

    def _insertOrUpdate(self, Object, table_name, fields, unique_keys, connection):
        with connections[connection].cursor() as cursor:
            fields_for_update = fields.copy()
            for f in unique_keys:
                fields_for_update.remove(f)

            values_for_update = []
            for f in fields:
                values_for_update.append(Object[f])
            for f in fields_for_update:
                values_for_update.append(Object[f])

            sql = "INSERT INTO {} \n".format(table_name) + \
                "({}) VALUES \n".format(",".join(["`{}`".format(f) for f in fields])) + \
                "({}) \n".format(", ".join(["%s"]*len(fields))) + \
                "ON DUPLICATE KEY UPDATE \n" + \
                (",".join(["`{}`=%s"]*len(fields_for_update))).format(*fields_for_update)

            if self.debug:
                logger.info("{}: SQL={}".format(connection, sql))
                logger.info("{}: values={}".format(connection, values_for_update))

            cursor.execute(sql, values_for_update)

            cursor.execute(
                "SELECT id FROM {} WHERE {}".format(
                    table_name, " AND ".join(["{}=%s"]*len(unique_keys)).format(*unique_keys)
                ),
                [Object[f] for f in unique_keys]
            )
            return cursor.fetchone()[0]
