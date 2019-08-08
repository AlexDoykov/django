import subprocess

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Currency, ExchangeRate
from .management.sync_fx_with_bnb_via_csv import sync_fx_with_bnb_via_csv


class ExchangeRateInline(admin.TabularInline):
    model = ExchangeRate
    extra = 0


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'iso_code', '_exchange_rate']
    list_filter = ('name',)
    fields = [('iso_code', 'name')]

    inlines = [
        ExchangeRateInline,
    ]

    def _exchange_rate(self, obj):
        return obj.exchange_rates.order_by('-valid_date').first().rate

    # _exchange_rate.empty_value_display = 'unknown'


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
        sync_fx_with_bnb_via_csv('https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm?download=csv&search=&lang=BG')

        # subprocess.run([
        #     'python',
        #     'manage.py',
        #     'sync_via_csv',
        #     'https://www.bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm?download=csv&search=&lang=BG'
        #     ])
        return HttpResponseRedirect('../')
