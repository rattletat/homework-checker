import os
import datetime
from .base import * # noqa
from .base import env

# GENERAL
# -------------------------------------------------------------------
DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CORS_ORIGIN_WHITELIST = env.list("DJANGO_ALLOWED_HOSTS")
LANGUAGE_CODE = "en"
USE_I18N = False
USE_L10N = True
USE_TZ = True

# EMAIL
# -------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# API
# -------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAdminUser"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
    "USER_ID_CLAIM": "id",
}

# SENDFILE
# -------------------------------------------------------------------

SENDFILE_BACKEND = "sendfile.backends.nginx"
