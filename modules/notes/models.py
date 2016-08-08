from django.db import models

from modules.utils.models import CRUDDateTimeModel


class Project(CRUDDateTimeModel):
    name = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Note(CRUDDateTimeModel):
    project = models.ForeignKey(Project)
    release_version = models.CharField(max_length=127)
    release_date = models.DateField(blank=True, null=True)
    release_link = models.URLField(blank=True, null=True)
    download_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["project__name", "-release_version"]

    def __str__(self):
        return "Notes for {} v. {}".format(self.project, self.release_version)
