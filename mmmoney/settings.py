import os
import sys

APP_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(APP_DIR)

DEBUG = any(
    (c in sys.argv for c in ('runserver', 'shell', 'dbshell', 'sql', 'sqlall'))
)

ADMINS = (
    ('Matthias Kestenholz', 'mk@feinheit.ch'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgres_psycopg2',
        'NAME': 'mmmoney',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'de-ch'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'towel.mt.middleware.LazyAccessMiddleware',
)

ROOT_URLCONF = 'mmmoney.urls'

WSGI_APPLICATION = 'mmmoney.wsgi.application'

LOCALE_PATHS = (
    os.path.join(os.path.dirname(APP_DIR), 'locale'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mmmoney',
    'towel_foundation',
    'towel',
    'django.contrib.admin',
)

TOWEL_MT_CLIENT_MODEL = 'mmmoney.Client'
TOWEL_MT_ACCESS_MODEL = 'mmmoney.Access'

LOGIN_REDIRECT_URL = '/'

try:
    from .local_settings import *  # noqa
except ImportError:
    pass
