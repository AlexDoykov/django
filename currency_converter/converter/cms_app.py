from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ConverterApphook(CMSApp):
    name = _("Converter Apphook")
    app_name = 'converter'

apphook_pool.register(ConverterApphook)