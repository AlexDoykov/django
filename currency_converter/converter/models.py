from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True)
    iso_code = models.CharField(max_length=5, unique=True)
    exchange_rate = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name + " " + self.iso_code

# class ExchangeRate(models.Model):
#     from_currency = models.ForeignKey(
#             Currency,
#             on_delete=models.CASCADE,
#             related_name='from_currency'
#         )
#     to_currency = models.ForeignKey(
#             Currency,
#             on_delete=models.CASCADE,
#             related_name='to_currency'
#         )
#     exchange_rate = models.DecimalField(max_digits=5, decimal_places=3)
#
#     def add_exchange_rate(from_currency, to_currency, exchange_rate):
#         from_currency_object = Currency.objects.get(id=1)
#         print(from_currency_object)
