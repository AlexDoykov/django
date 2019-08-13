from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CurrencyManager(models.Manager):
    def get_currencies_by_date(self, date):
        return self.get_queryset().filter(
            exchange_rates__valid_date=date
            ).values_list('id', 'name', 'iso_code', 'exchange_rates__rate')


class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    iso_code = models.CharField(
        max_length=5,
        unique=True,
        verbose_name=_('iso code')
        )
    objects = CurrencyManager()

    class Meta:
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __str__(self):
        return self.name + ' ' + self.iso_code

    def get_latest_rate(self):
        return self.exchange_rates.order_by('-valid_date').first().rate


class ExchangeRateManager(models.Manager):
    def get_latest_date(self):
        latest_date = self.get_queryset().order_by(
            '-valid_date'
            ).values('valid_date').first()
        if latest_date is None:
            return latest_date
        else:
            return latest_date.get('valid_date')


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
    valid_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('valid date')
        )

    objects = ExchangeRateManager()

    class Meta:
        verbose_name = _('exchange rate')
        verbose_name_plural = _('exchange rates')
        unique_together = (('valid_date', 'currency'),)
        permissions = [
            ('update_exchange_rates', 'user can update exchange rates')
        ]
