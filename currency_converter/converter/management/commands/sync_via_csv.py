import requests

from django.core.management.base import BaseCommand

from converter.models import ExchangeRate


class Command(BaseCommand):
    def download_file(self, url):
        return requests.get(url, allow_redirects=True)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('url', type=str)

    def handle(self, *args, **kwargs):
        downloaded_csv = self.download_file(kwargs['url'])
        decoded_csv = downloaded_csv.content.decode('utf-8')
        splitted_csv = decoded_csv.split('\n')
        currencies = splitted_csv[2:33]
        for currency in currencies:
            currency_elements = currency.split(',')
            date = currency_elements[0]
            name = currency_elements[1]
            iso_code = currency_elements[2]
            exchange_rate = currency_elements[4]
            ExchangeRate.save_to_db_once_per_day(
                exchange_rate,
                name,
                iso_code,
                date
                )

        self.stdout.write(self.style.SUCCESS('Successfully downloaded file'))
