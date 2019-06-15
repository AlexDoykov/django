from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True)
    iso_code = models.CharField(max_length=5, unique=True)
    exchange_rate = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name + " " + self.iso_code
