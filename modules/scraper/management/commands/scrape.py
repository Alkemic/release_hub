from django.core.management.base import BaseCommand
from importlib import import_module


class Command(BaseCommand):
    help = "Run single scraper"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        scraper_module = import_module("scraper.{}".format(options["name"]))
        notes = scraper_module.Scrapper().initial()

        for item in notes:
            print("{date} | {version} | {url} ".format(**item))
