# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models import Manager


class ActiveManager(Manager):

    def get_queryset(self):
        return super(ActiveManager, self).get_queryset()\
            .filter(deleted_at__isnull=True)

    def active(self, pk=False, slug=False):
        """ Zwraca aktywne newsy """
        base_qs = self.get_queryset().filter(activated_at__isnull=False)\
            .filter(created_at__lte=datetime.now())

        if slug and pk:
            return base_qs.get(pk=pk, slug=slug)
        elif slug:
            return base_qs.get(slug=slug)
        elif pk:
            return base_qs.get(pk=pk)

        return base_qs

    def unactive(self):
        """ Zwraca nieaktywne newsy """
        base_qs = self.get_queryset().filter(activated_at__isnull=True)\
            .filter(created_at__lte=datetime.now())

        return base_qs

    def deleted(self):
        """ Zwraca nieusunięte newsy """
        return super(ActiveManager, self).get_queryset()\
            .filter(deleted_at__isnull=False)
