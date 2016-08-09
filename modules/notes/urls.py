from django.conf.urls import *
from django.views.decorators.cache import cache_page

from .views import NotesList, EntryView


urlpatterns = [
    url(
        r'(?P<project_name>.*)_(?P<project_version>.*).html$',
        cache_page(60 * 60 * 24)(EntryView.as_view()),
        name='entry',
    ),
    url(r"$", cache_page(60 * 60 * 24)(NotesList.as_view()), name="index"),
]

