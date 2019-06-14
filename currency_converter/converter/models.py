from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=20)
    iso_code = models.CharField(max_length=5)
    exchange_rate = models.ManyToManyField(
            'self',
            through='ExchangeRate',
            symmetrical=False
        )

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(
            Currency,
            on_delete=models.CASCADE,
            related_name='from_currency'
        )
    to_currency = models.ForeignKey(
            Currency,
            on_delete=models.CASCADE,
            related_name='to_currency'
        )
    exchange_rate = models.DecimalField(max_digits=5, decimal_places=3)

    def add_exchange_rate(from_currency, to_currency, exchange_rate):
        from_currency_object = Currency.objects.get(id=1)
        print(from_currency_object)

    def __str__(self):
        return str(self.from_currency) + " " + str(self.to_currency) + " " + str(self.exchange_rate)
