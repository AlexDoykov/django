import requests
import csv
import os
from datetime import datetime

from converter.models import ExchangeRate, Currency


def save_file(url):
    file = requests.get(url, allow_redirects=True)
    with open("exchange_rates.csv", 'w') as f:
        f.write(file.content.decode("utf-8"))


def sync_fx_with_bnb_via_csv(url):
    save_file(url)
    with open("exchange_rates.csv", 'r') as f:
        file = f.readlines()
        reader = csv.reader(file[2:33])
        for exchange_rate in reader:
            date = exchange_rate[0]
            name = exchange_rate[1]
            iso_code = exchange_rate[2]
            exchange_rate = exchange_rate[4]
            currency = Currency.objects.get_or_create(
                name=name,
                iso_code=iso_code
                )
            ExchangeRate.objects.get_or_create(
                rate=exchange_rate,
                currency=currency[0],
                valid_date=datetime.strptime(date, "%d.%m.%Y").date()
                )
    os.remove("exchange_rates.csv")
