from django.core.management.base import BaseCommand
from converter.models import Currency
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
        for element in table:
            currency_name = element.contents[1].contents[0]
            currency_iso_code = element.contents[3].contents[0]
            currency_exchange_rate = element.contents[7].contents[0]
            Currency.change_db(
                    currency_name,
                    currency_iso_code,
                    currency_exchange_rate
                    )
        self.stdout.write(self.style.SUCCESS('Successfully downloaded file'))
