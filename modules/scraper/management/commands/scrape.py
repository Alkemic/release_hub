from django.core.management.base import BaseCommand
from importlib import import_module

from modules.utils.classes import BaseScrapper


class Command(BaseCommand):
    help = "Run single scraper"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        module_name = "scraper.{}".format(options["name"])
        scraper_module = import_module(module_name)

        if not issubclass(scraper_module.Scrapper, BaseScrapper):
            self.stderr.write(
                "`{}.Scrapper` must be instance of `{}.BaseScrapper`".format(
                    module_name, BaseScrapper.__module__,
                ),
            )
            exit(1)

        notes = scraper_module.Scrapper().initial()

        for item in notes:
            print("{date} | {version} | {url} ".format(**item))
