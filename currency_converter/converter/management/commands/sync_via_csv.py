from django.core.management.base import BaseCommand

from converter.management.sync_fx_with_bnb_via_csv import \
    sync_fx_with_bnb_via_csv


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **kwargs):
        sync_fx_with_bnb_via_csv(kwargs['url'])

        self.stdout.write(self.style.SUCCESS('Successfully downloaded file'))
