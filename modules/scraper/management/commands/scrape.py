from datetime import datetime
from importlib import import_module

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from modules.notes.models import Project, Note
from modules.utils.classes import BaseScrapper

User = get_user_model()


class Command(BaseCommand):
    help = "Run single scraper"

    _user = User.objects.get(username="alkemic")

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        parser.add_argument("--execute", action="store_true")

    def _get_project(self, scraper):
        return Project.objects.get_or_create(
            name=scraper.project_name,
            created_by=self._user,
        )[0]

    def _save_notes(self, scraper, note, project):
        note_obj, _ = Note.objects.get_or_create(
            project=project,
            release_version=note["version"],
            created_by=self._user,
        )

        note_obj.activated_by = self._user
        note_obj.activated_at = datetime.now()

        note_obj.release_date = note["date"]
        note_obj.release_link = note["url"]
        note_obj.download_link = note.get("download")
        note_obj.notes = note["notes"]
        note_obj.save()

        return note_obj

    def handle(self, *args, **options):
        execute = options["execute"]
        module_name = "scraper.{}".format(options["name"])
        scraper_module = import_module(module_name)

        if not issubclass(scraper_module.Scrapper, BaseScrapper):
            self.stderr.write(
                "`{}.Scrapper` must be instance of `{}.BaseScrapper`".format(
                    module_name, BaseScrapper.__module__,
                ),
            )
            exit(1)

        scraper = scraper_module.Scrapper()
        notes = scraper.initial()

        project = self._get_project(scraper) if execute else None

        for item in notes:
            print("{date} | {version} | {url} ".format(**item))
            if execute:
                self._save_notes(scraper, item, project)
