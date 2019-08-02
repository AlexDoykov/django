from django.core.management.base import BaseCommand
from converter.models import Currency, ExchangeRate
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    def download_file(self):
            url = 'http://bnb.bg/Statistics/StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm'
            return requests.get(url, allow_redirects=True)

    def handle(self, *args, **kwargs):
        downloaded_html = self.download_file()
        html_string = downloaded_html.content.decode("utf-8")
        soup = BeautifulSoup(html_string, 'html.parser')
        table = soup.find_all("tr")
        table = table[1:]
        table = table[:-2]
        for currency in table:
            name = currency.contents[1].contents[0]
            iso_code = currency.contents[3].contents[0]
            exchange_rate = currency.contents[7].contents[0]

            ExchangeRate.save_to_db_once_per_day(exchange_rate, name, iso_code)

        self.stdout.write(self.style.SUCCESS('Successfully downloaded file'))
