from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConverterConfig(AppConfig):
    name = 'converter'
    verbose_name = _('converter')
