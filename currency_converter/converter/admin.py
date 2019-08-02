from django.contrib import admin
from .models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["name", "iso_code", "exchange_rate"]
    list_filter = ("name", "exchange_rate")
    fields = [("iso_code", "name"), "exchange_rate"]
