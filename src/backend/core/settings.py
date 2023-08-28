# -*- coding: utf-8 -*-
"""
Django settings for swissmooc-exxtras project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os

from decouple import config
from decouple import Csv
from unipath import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY", default="qdtzo2b!r^ux*8h37dxx1b3qq@#oawbk(pi7l!k%sb+1x9l023"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

MODE = config("MODE", default="staging")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.edx",
    "rest_framework",
    "apps.home",
    "apps.check_ssl",
    "apps.split_logs",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

SOCIALACCOUNT_PROVIDERS = {
    "edx": {
        "EDX_URL": config(
            "SOCIALACCOUNT_PROVIDERS_EDX_URL", default="https://id.test-swissmooc.ch"
        ),
    }
}

TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

INSTANCES = config("INSTANCES", cast=Csv())
SWARMS = config('SWARMS', cast=Csv())
BACKUP_SERVER = config('BACKUP_SERVER')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_DATABASE"),
        "USER": config("MYSQL_USER"),
        "PASSWORD": config("MYSQL_PASSWORD"),
        "HOST": config("MYSQL_DATABASE_HOST", default="db"),
        "PORT": config("MYSQL_DATABASE_PORT", default=3306),
        "OPTIONS": {
            "charset": "utf8mb4",
            "sql_mode": "STRICT_TRANS_TABLES",
        },
    },
}

EDXAPP_DATABASES = {
    'readonly': {
        'host': config("EDXAPP_MYSQL_HOST"),
        'user': config("EDXAPP_MYSQL_USER"),
        'password': config("EDXAPP_MYSQL_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/data/static"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [
            config("CACHE_LOCATION", f"redis://{config('REDIS_HOST')}:6379"),
        ],
    }
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_VERIFICATION = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        #'logfile': {
        #    'level': 'INFO',
        #    'class': 'logging.FileHandler',
        #    'filename': os.path.join(
        #        '/var', 'log', 'swissmooc-extras', 'django.log'
        #    ),
        #},
        #'mail_admins': {
        #    'level': 'ERROR',
        #    'class': 'django.utils.log.AdminEmailHandler',
        #    # 'filters': ['special']
        #}
    },
    'loggers': {
        # Redefining the logger for the `django` module
        # prevents invoking the `AdminEmailHandler`
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        '': {
            #'handlers': ['logfile'],
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'split_logs': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'WARNING',
        },
        'check_ssl': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'WARNING',
        },
        # 'split_logs.management.commands': {
        #     'handlers': ['mail_admins'],
        #     'propagate': False,
        #     'level': 'ERROR',
        # },
    }
}

TRACKING_LOGS_ORIGINAL_SRC=config("TRACKING_LOGS_ORIGINAL_SRC")
TRACKING_LOGS_ORIGINAL_DST=config("TRACKING_LOGS_ORIGINAL_DST")
TRACKING_LOGS_ORIGINAL_DOCKER_SRC=config("TRACKING_LOGS_ORIGINAL_DOCKER_SRC")
TRACKING_LOGS_ORIGINAL_DOCKER_DST=config("TRACKING_LOGS_ORIGINAL_DOCKER_DST")
TRACKING_LOGS_SPLITTED=config("TRACKING_LOGS_SPLITTED")
TRACKING_LOGS_SPLITTED_DOCKER=config("TRACKING_LOGS_SPLITTED_DOCKER")
TRACKING_LOGS_ENCRYPTED=config("TRACKING_LOGS_ENCRYPTED")
TRACKING_LOGS_ENCRYPTED_DOCKER=config("TRACKING_LOGS_ENCRYPTED_DOCKER")
DUMP_DB_PATH=config("DUMP_DB_PATH")
DUMP_XML_PATH=config("DUMP_XML_PATH")

STATS_FILE_PATH=config("STATS_FILE_PATH")

SMS_APP_ENV=config("SMS_APP_ENV")

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = config("AWS_QUERYSTRING_AUTH", False)
AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = config("AWS_S3_CUSTOM_DOMAIN")
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")
AWS_STORAGE_BUCKET_NAME_ANALYTICS='{env}-analytics'.format(env=SMS_APP_ENV)

EMAIL_FROM_ADDRESS = 'noreply-courseware@epfl.ch'
EMAIL_TO_ADDRESSES = ['edx-monitor@groupes.epfl.ch']

MONGODB_HOST = config("MONGODB_HOST")
MONGODB_USER = config("MNGODB_USER", "admin")
MONGODB_PASSWORD = config("MONGODB_PASSWORD")
