from django.contrib import admin
from .models import Currency, ExchangeRate


class ExchangeRateInline(admin.TabularInline):
    model = ExchangeRate
    extra = 0


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "iso_code", "_exchange_rates"]
    list_filter = ("name",)
    fields = [("iso_code", "name")]

    inlines = [
        ExchangeRateInline,
    ]

    def _exchange_rates(self, obj):
        return obj.exchange_rates.all().count()


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ["rate", "currency", "valid_date"]
    list_filter = ("currency",)


""" това дали изобщо ми трябва    list_select_related = (
        "currency",
    ) """
