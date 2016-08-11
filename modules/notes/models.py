import re

from django.db import models
from django.db.models import permalink

from modules.utils.functions import generate_orderable_version_number
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
    release_version_order = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True)
    release_link = models.URLField(blank=True, null=True)
    download_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["project__name", "-release_version_order"]

    def __str__(self):
        return "Notes for {} v. {}".format(self.project, self.release_version)

    @permalink
    def get_absolute_url(self):
        return "notes:entry", (self.project.name, self.release_version)

    def get_prev_in_project(self):
        try:
            self.__prev_in_project = Note.objects.active() \
                .order_by("-release_version_order") \
                .filter(project=self.project) \
                .filter(release_version_order__lt=self.release_version_order) \
                .first()
        except Note.DoesNotExist:
            self.__prev_in_project = None

        return self.__prev_in_project

    def get_next_in_project(self):
        try:
            self.__next_in_project = Note.objects.active() \
                .order_by("release_version_order") \
                .filter(project=self.project) \
                .filter(release_version_order__gt=self.release_version_order) \
                .first()

        except Note.DoesNotExist:
            self.__next_in_project = None

        return self.__next_in_project

    def save(self, *args, **kwargs):
        self.release_version_order = generate_orderable_version_number(
            self.release_version,
        )

        super().save(*args, **kwargs)
