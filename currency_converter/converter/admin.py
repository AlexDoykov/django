from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.translation import ugettext_lazy as _

from .management.sync_fx_with_bnb_via_csv import sync_fx_with_bnb_via_csv
from .models import Currency, ExchangeRate


class ExchangeRateInline(admin.TabularInline):
    model = ExchangeRate
    extra = 0


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'iso_code', '_exchange_rate', 'slug']
    list_filter = ('name',)
    fields = [('iso_code', 'name')]

    inlines = [
        ExchangeRateInline,
    ]

    def _exchange_rate(self, obj):
        exchange_rate = obj.exchange_rates.order_by('-valid_date').first()
        if exchange_rate is None:
            return exchange_rate
        return exchange_rate.rate
    _exchange_rate.short_description = _("Exchange rate")



@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['rate', 'currency', 'valid_date']
    list_filter = ('currency',)
    date_hierarchy = 'valid_date'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                'update_exchange_rates/',
                self.admin_site.admin_view(self.update_exchange_rates),
                name='update_exchange_rates'
                )
        ]
        return my_urls + urls

    def update_exchange_rates(self, request):
        # if request.user.is_superuser:
        # if request.user.has_perm('converter.update_exchange_rates'):
        if self.has_view_permission(request, ExchangeRate):
            sync_fx_with_bnb_via_csv('https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm?download=csv&search=&lang=BG')
        return HttpResponseRedirect('../')
