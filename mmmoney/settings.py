import os
import sys
from pathlib import Path

from speckenv import env
from speckenv_django import django_database_url


DEBUG = env("DEBUG", required=True)
TESTING = any(r in sys.argv for r in ("test",))
LIVE = env("LIVE", default=False)
ALLOWED_HOSTS = env("ALLOWED_HOSTS", required=True)
SECURE_SSL_HOST = env("SECURE_SSL_HOST", default="")
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", default=False, warn=True)
BASE_DIR = Path(__file__).resolve().parent.parent

ADMINS = (("Matthias Kestenholz", "mk@feinheit.ch"),)
MANAGERS = ADMINS

SERVER_EMAIL = "root@oekohosting.ch"

DATABASES = {"default": django_database_url(env("DATABASE_URL", required=True))}
# CACHES = {"default": django_cache_url(env("CACHE_URL", required=True))}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SECRET_KEY = env("SECRET_KEY", required=True)

TIME_ZONE = "Europe/Zurich"
LANGUAGE_CODE = "de-ch"
SITE_ID = 1
USE_I18N = True
USE_TZ = True
MEDIA_ROOT = ""
MEDIA_URL = ""
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MIDDLEWARE = (
    "canonical_domain.middleware.canonical_domain",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "towel.mt.middleware.LazyAccessMiddleware",
)

ROOT_URLCONF = "mmmoney.urls"

WSGI_APPLICATION = "wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mmmoney",
    "canonical_domain",
    "towel",
    "django.contrib.admin",
)

TOWEL_MT_CLIENT_MODEL = "mmmoney.Client"
TOWEL_MT_ACCESS_MODEL = "mmmoney.Access"

LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "authlib.backends.EmailBackend",
)

GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET")

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

if SECURE_SSL_REDIRECT:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 7 * 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
