from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Project, Note


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = "project", "release_version", "release_date", "is_activated"
    list_display_links = "project", "release_version"
    list_filter = "project",

    date_hierarchy = "release_date"

    fields = "project", "release_version", "release_date", "release_link", \
             "download_link", "notes", "notes_html",
    readonly_fields = "notes_html",

    def notes_html(self, obj):
        return mark_safe(obj.notes)
