from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ContributorsConfig(AppConfig):
    name = "apps.contributors"
    verbose_name = _("Contributors")
