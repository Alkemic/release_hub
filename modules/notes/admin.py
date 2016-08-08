from django.contrib import admin

from .models import Project, Note


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass
