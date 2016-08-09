from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.translation import ugettext_lazy as _

from modules.utils.mixins import BreadcrumbsMixin

from .models import Note, Project


class NotesList(BreadcrumbsMixin, ListView):
    """Displays list of relese notes"""
    template_name = 'notes/index.html'
    context_object_name = 'list'
    queryset = Note.objects.active()
    paginate_by = 25

    breadcrumbs = (
        (_('Notes'), reverse_lazy('notes:index')),
    )


class EntryView(BreadcrumbsMixin, DetailView):
    """Display single release note"""
    template_name = 'notes/entry.html'
    context_object_name = 'entry'
    queryset = Note.objects.active()

    @property
    def breadcrumbs(self):
        if not hasattr(self, 'object') or self.object is None:
            self.object = self.get_object()

        return (
            (_('Notes'), reverse_lazy('notes:index')),
            ('%s' % self.object, self.object.get_absolute_url()),
        )

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        project = Project.objects.get(name=self.kwargs.get("project_name"))
        obj = queryset.get(
            release_version=self.kwargs.get("project_version"),
            project=project,
        )

        return obj
