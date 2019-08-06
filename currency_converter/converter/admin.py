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
        return obj.exchange_rates.order_by("-valid_date").first().rate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ["rate", "currency", "valid_date"]
    list_filter = ("currency",)
    date_hierarchy = "valid_date"
