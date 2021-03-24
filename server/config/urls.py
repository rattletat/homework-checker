from core import api_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include(api_urls)),
    path("django-rq/", include("django_rq.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
]
