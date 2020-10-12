from django.contrib import admin
from django.urls import include, path

from apps.api import urls as api_urls
from apps.teaching import urls as teaching_urls
from apps.teaching.views import home_view

urlpatterns = [
    path("", home_view),
    path("teaching/", include(teaching_urls)),
    path("api/", include(api_urls)),
    path("admin/", admin.site.urls),
]
