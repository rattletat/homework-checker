from core import api_urls
from django.conf import settings
from django.contrib import admin
import django_rq
from django.urls import include, path

admin.site.site_header = 'Homework Checker'
admin.site.index_title = 'Admin Portal'
admin.site.site_title = 'Homework Checker'

urlpatterns = [
    path("api/", include(api_urls)),
    path(settings.RQ_URL, include("django_rq.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
]
