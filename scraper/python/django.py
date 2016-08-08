import re

import requests
import scrapper

from modules.utils.classes import BaseScrapper
from modules.utils.functions import extract_version, extract_date


class DjangoReleaseNote(scrapper.CrawlerItem):
    version = scrapper.CrawlerField(
        "#docs-content > .section > h1",
        lambda value, _, __:
            extract_version(value.text.replace(" release notes", "")),
        True,
    )
    date = scrapper.CrawlerField(
        "#docs-content > .section > p > em",
        lambda value, _, __: extract_date(value.strip()) if value else None,
    )
    notes = scrapper.CrawlerField(
        "#docs-content > .section > *",
        lambda _, content, __: "\n".join([
            str(sec)
            for sec in content.select(".section")
        ]),
        True,
    )
    url = scrapper.CrawlerField("#asd", lambda _, __, response: response.url)


def release_notes_links(tag):
    return tag.name == "a" and re.search("Django .* release notes", tag.text)


class DjangoReleaseNoteSet(scrapper.CrawlerItemSet):
    DJANGO_DOCS_URL = "https://docs.djangoproject.com/"
    url = "{}releases/".format(requests.get(DJANGO_DOCS_URL).url)
    base_url = url
    item_class = DjangoReleaseNote
    links_selector = release_notes_links,


class Scrapper(BaseScrapper):
    project_name = "Django"

    def initial(self):
        for note in DjangoReleaseNoteSet():
            yield note.as_dict()
