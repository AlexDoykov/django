from datetime import datetime

from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    iso_code = models.CharField(
        max_length=5,
        unique=True,
        verbose_name=_('iso code')
        )

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __str__(self):
        return self.name + ' ' + self.iso_code

    @staticmethod
    def add_currency(name, iso_code):
        new_currency = Currency(
                name=name,
                iso_code=iso_code,
                )
        new_currency.save()
        return new_currency

    @staticmethod
    def get_currency_with_rates(id):
        return Currency.objects.select_related().get(id=id)

    @staticmethod
    def get_currencies_by_date(date):
        return Currency.objects.filter(
            exchange_rates__valid_date=date
            ).values_list(
            'id',
            'name',
            'iso_code',
            'exchange_rates__rate'
            )

    def get_latest_rate(self):
        return self.exchange_rates.order_by('-valid_date').first().rate


class ExchangeRate(models.Model):
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        verbose_name=_('rate')
        )
    currency = models.ForeignKey(
        'Currency',
        on_delete=models.CASCADE,
        related_name='exchange_rates',
        verbose_name=_('currency')
        )
    valid_date = models.DateField(
        default=timezone.now,
        verbose_name=_('valid date')
        )

    class Meta:
        verbose_name = _('exchange rate')
        verbose_name_plural = _('exchange rates')

    @staticmethod
    def save_to_db_once_per_day(
        rate,
        currency_name,
        currency_iso_code,
        currency_date
    ):
        latest_date = ExchangeRate.get_latest_date()
        saved_today = ExchangeRate.objects.filter(
            currency__name=currency_name,
            valid_date=latest_date
            ).exists()
        if not saved_today:
            ExchangeRate.save_to_db(
                rate,
                currency_name,
                currency_iso_code,
                currency_date
                )
        else:
            print("This was already updated today.")

    @staticmethod
    def save_to_db(rate, currency_name, currency_iso_code, currency_date):
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
        new_exchange_rate = ExchangeRate(
            rate=rate,
            currency=currency,
            valid_date=datetime.strptime(currency_date, "%d.%m.%Y").date()
            )
        new_exchange_rate.save()

    @staticmethod
    def get_latest_date():
        date_dict = ExchangeRate.objects.order_by("-valid_date").values(
            "valid_date"
            ).first()

        # maybe something better here

        if date_dict is None:
            return None
        else:
            return date_dict["valid_date"]
