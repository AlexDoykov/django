from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True)
    iso_code = models.CharField(max_length=5, unique=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=7)

    def __str__(self):
        return self.name + " " + self.iso_code

    @staticmethod
    def update(
            name,
            iso_code,
            exchange_rate,
            count_by_name,
            count_by_iso_code
            ):
        if count_by_name > 0 and count_by_iso_code > 0:
            db_currency = Currency.objects.get(name=name)
        if count_by_name > 0 and count_by_iso_code == 0:
            db_currency = Currency.objects.get(name=name)
            db_currency.iso_code = iso_code
        else:
            db_currency = Currency.objects.get(iso_code=iso_code)
            db_currency.name = name
        db_currency.exchange_rate = exchange_rate
        db_currency.save()

    def create(name, iso_code, exchange_rate):
        db_currency = Currency(
                name=name,
                iso_code=iso_code,
                exchange_rate=exchange_rate,
                )
        db_currency.save()

    @staticmethod
    def change_db(name, iso_code, exchange_rate):
        count_by_name = Currency\
            .objects.filter(name=name).count()
        count_by_iso_code = Currency\
            .objects.filter(iso_code=iso_code).count()

        if count_by_name > 0 or count_by_iso_code > 0:
            Currency.update(
                    name,
                    iso_code,
                    exchange_rate,
                    count_by_name,
                    count_by_iso_code
                    )
        else:
            Currency.create(name, iso_code, exchange_rate)


class NotSerializable(models.Model):
    pass
