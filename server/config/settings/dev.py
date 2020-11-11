from .base import *  # noqa
import datetime

# GENERAL
# -------------------------------------------------------------------
DEBUG = True
SECRET_KEY = "weak-key"
ALLOWED_HOSTS = ["*"]

# CACHES
# -------------------------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# -------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# API
# -------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "USER_ID_CLAIM": "id",
}

# SENDFILE
# -------------------------------------------------------------------

SENDFILE_BACKEND = "sendfile.backends.development"

# CORSHEADERS
# -------------------------------------------------------------------

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3001",
]
