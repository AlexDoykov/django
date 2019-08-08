from django.core.management.base import BaseCommand
from converter.models import Currency, ExchangeRate
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.SUCCESS('Successfully downloaded file'))
