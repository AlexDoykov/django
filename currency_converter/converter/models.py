from django.db import models
from datetime import date


class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True)
    iso_code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Currencies'

    @staticmethod
    def add_currency(name, iso_code):
        new_currency = Currency(
                name=name,
                iso_code=iso_code,
                )
        new_currency.save()
        return new_currency


class ExchangeRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=7)
    currency = models.ForeignKey(
        "Currency",
        on_delete=models.CASCADE,
        related_name="exchange_rates"
        )
    valid_date = models.DateField(auto_now_add=True)

    @staticmethod
    def save_to_db_once_per_day(rate, currency_name, currency_iso_code):
        saved_today = ExchangeRate.objects.filter(
            currency__name=currency_name,
            valid_date__range=(
                date.today(),
                date.today()
                )
            ).exists()
        if not saved_today:
            ExchangeRate.save_to_db(rate, currency_name, currency_iso_code)
        else:
            print("This was already updated today.")

    @staticmethod
    def save_to_db(rate, currency_name, currency_iso_code):
        currency_exists = Currency.objects.filter(
            name=currency_name,
            iso_code=currency_iso_code
            ).exists()
        if currency_exists:
            currency = Currency.objects.get(name=currency_name)
        else:
            currency = Currency.add_currency(
                currency_name,
                currency_iso_code,
                )
        new_exchange_rate = ExchangeRate(rate=rate, currency=currency)
        new_exchange_rate.save()
