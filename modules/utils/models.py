from datetime import datetime

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from .managers import ActiveManager


class CRUDDateTimeModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Who created",
        related_name="%(app_label)s_%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Who updated",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_updated"
    )
    activated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Who activated",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_activated",
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Who deleted",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_deleted",
    )

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    activated_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    objects = ActiveManager()

    def is_activated(self):
        return self.activated_at is not None

    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def do_delete(self, request, *args, **kwargs):
        self.deleted_at = datetime.now()
        self.deleted_by = request.user

        self.save(*args, **kwargs)

    def do_undelete(self, request, *args, **kwargs):
        self.deleted_at = None
        self.deleted_by = None

        self.save(*args, **kwargs)

    def do_save(self, request, *args, **kwargs):
        if self.pk:
            self.updated_by = request.user
            self.updated_at = datetime.now()
        else:
            self.created_by = request.user
            self.created_at = datetime.now()

        self.save(*args, **kwargs)

    def do_activate(self, request, *args, **kwargs):
        self.activated_at = datetime.now()
        self.activated_by = request.user

        self.save(*args, **kwargs)

    def next_entry(self):
        try:
            self.__next_entry = self.__class__.objects.active().\
                get(pk=self.pk).get_next_by_date()
        except self.__class__.DoesNotExist:
            self.__next_entry = None

        return self.__next_entry

    def prev_entry(self):
        try:
            self.__prev_entry = self.__class__.objects.active()\
                .get(pk=self.pk).get_previous_by_date()
        except self.__class__.DoesNotExist:
            self.__prev_entry = None

        return self.__prev_entry

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.save()

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = datetime.now()
        elif not self.created_at:
            self.created_at = datetime.now()

        super(CRUDDateTimeModel, self).save(*args, **kwargs)


class AbstractBaseModel(CRUDDateTimeModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta(CRUDDateTimeModel.Meta):
        abstract = True
        # ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "%s:entry" % self._meta.app_label,
            args=(self.id, self.slug),
        )
