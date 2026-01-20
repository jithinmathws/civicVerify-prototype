from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EvidenceConfig(AppConfig):
    name = "apps.evidence"
    verbose_name = _("Evidence")
