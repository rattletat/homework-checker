import os
from .base import *

# GENERAL
# -------------------------------------------------------------------
DEBUG = True
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
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
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAdminUser"],
}
