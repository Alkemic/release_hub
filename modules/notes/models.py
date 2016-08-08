from django.db import models

from modules.utils.models import CRUDDateTimeModel


class Project(CRUDDateTimeModel):
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        ordering = ["-name"]


class Note(CRUDDateTimeModel):
    project = models.ForeignKey(Project)
    release_version = models.CharField(max_length=127)
    release_date = models.DateField()
    release_link = models.URLField()
    download_link = models.URLField()
    notes = models.TextField()

    class Meta:
        ordering = ["-project", "release_version"]
