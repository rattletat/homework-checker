from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from core import api_urls

urlpatterns = [
    path("api/", include(api_urls)),
    path("admin/", admin.site.urls),
]
