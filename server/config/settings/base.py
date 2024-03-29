"""
Base settings to build other settings files upon.
"""
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = ROOT_DIR / "apps"
env = environ.Env()


# GENERAL
# -------------------------------------------------------------------
LANGUAGES = (
    ("en", _("English")),
    # ("de", _("German")),
)
DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "Europe/Berlin"
LANGUAGE_CODE = "en-us"
SITE_ID = env("DJANGO_SITE_ID", default=1)
USE_I18N = True
USE_L10N = True
USE_TZ = True
# LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# DATABASES
# -------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("POSTGRES_HOST", default=""),
        "PORT": env("POSTGRES_PORT", default=""),
        "USER": env("POSTGRES_USER", default=""),
        "PASSWORD": env("POSTGRES_PASSWORD", default=""),
        "NAME": env("POSTGRES_DB", default=""),
    }
}

# URLS
# -------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.routing.application"

# APPS
# -------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.postgres",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = ["corsheaders", "rest_framework", "django_rq"]
LOCAL_APPS = ["apps.accounts", "apps.teaching", "apps.homework", "apps.flatpages"]
SPECIAL_APPS = ["django_cleanup"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + SPECIAL_APPS


# AUTHENTICATION
# -------------------------------------------------------------------
# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
# ]
AUTH_USER_MODEL = "accounts.CustomUser"
# LOGIN_REDIRECT_URL = "users:redirect"
# LOGIN_URL = "account_login"

# PASSWORDS
# -------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {"user_attributes": ("email", "name", "identifier")},
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    {"NAME": "apps.accounts.validators.HasLowerCaseValidator"},
    {"NAME": "apps.accounts.validators.HasUpperCaseValidator"},
    {"NAME": "apps.accounts.validators.HasNumberValidator"},
]

# MIDDLEWARE
# -------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# -------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/staticfiles/"
# STATICFILES_DIRS = [str(ROOT_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA
# -------------------------------------------------------------------
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

# TEMPLATES
# -------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(ROOT_DIR / "templates")],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# SECURITY
# -------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# EMAIL
# -------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_TIMEOUT = 5

# ADMIN
# -------------------------------------------------------------------
ADMIN_URL = env("DJANGO_ADMIN_URL")
ADMINS = []
MANAGERS = ADMINS

# LOGGING
# -------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# REDIS QUEUES
# -------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "MAX_ENTRIES": 5000,
        },
    },
}
RQ_QUEUES = {
    "default": {
        "HOST": env("REDIS_HOST"),
        "PORT": env("REDIS_PORT"),
        "DB": env("REDIS_DB"),
        "DEFAULT_TIMEOUT": env.int("REDIS_TIMEOUT"),
    },
}
RQ_SHOW_ADMIN_LINK = True
RQ_URL = env("DJANGO_RQ_URL")

# SENDFILE
# -------------------------------------------------------------------
SENDFILE_ROOT = MEDIA_ROOT
SENDFILE_URL = MEDIA_URL
