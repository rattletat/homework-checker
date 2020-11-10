from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TeachingConfig(AppConfig):
    name = "apps.teaching"
    verbose_name = _("Lehre")
