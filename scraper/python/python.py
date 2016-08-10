import re

import scrapper
import requests
from markdown import markdown

from modules.utils.classes import BaseScrapper
from modules.utils.functions import extract_version, extract_date


class ReleaseEntry(scrapper.CrawlerItem):
    version = scrapper.CrawlerField(
        "span.release-number > a",
        lambda value, content, response:
            value.strip().replace("Python ", "") if value else None,
    )
    date = scrapper.CrawlerField(
        "span.release-date",
        lambda value, content, response: value.strip()if value else None,
    )
    sources_url = scrapper.CrawlerField(
        "span.release-download > a",
        lambda value, content, response: value["href"] if value else None,
        True,
    )
    url = scrapper.CrawlerField(
        "span.release-enhancements > a",
        lambda value, content, response: value["href"] if value else None,
        True,
    )


class ReleaseEntryCollection(scrapper.CrawlerMultiItem):
    item_class = ReleaseEntry
    content_selector = ".list-row-container.menu li"


class ReleaseSection(scrapper.CrawlerItem):
    version = scrapper.CrawlerField(
        "h2",
        lambda value, content, response: extract_version(value.text),
        True,
    )
    date = scrapper.CrawlerField(
        "p",
        lambda value, _, __: extract_date(value.strip()) if value else None,
    )
    notes = scrapper.CrawlerField(
        "*",
        lambda _, content, __: "\n".join([
            str(sec)
            for sec in content.select(".section > .section")
        ]),
        True,
    )


class ReleaseSectionCollection(scrapper.CrawlerMultiItem):
    item_class = ReleaseSection
    content_selector = ".body > .section > .section"


class Scrapper(BaseScrapper):
    project_name = "Python"

    downloads_url = "https://www.python.org/downloads/"

    HG_RELEASE_HEADER = "(What's New in Python .*\n=*\n\n.*Release date.*\n\n)"

    def initial(self):
        item_set = ReleaseEntryCollection(self.downloads_url)
        for item in item_set:
            if item.url.startswith("https://docs.python.org"):
                yield from self._parse_pydocs(item)

            elif item.url.startswith("https://hg.python.org/") or \
                    item.url.startswith("http://hg.python.org/"):
                yield from self._parse_hg(item)

    def _decode_cnt(self, text):
        try:
            return text.decode()
        except UnicodeDecodeError:
            # brute-force encoding...
            for enc in ["latin2"]:
                try:
                    text = str(text, enc)
                    return text
                except UnicodeDecodeError:
                    pass

        raise ValueError

    def _parse_pydocs(self, item):
        notes_set = ReleaseSectionCollection(item.url)

        for note in filter(lambda el: item.version in el.version, notes_set):
            yield {
                "version": note.version,
                "notes": note.notes,
                "date": note.date,
                "url": item.url,
            }

    def _parse_hg(self, item):
        resp = requests.get(item.url)
        cnt = self._decode_cnt(resp.content)

        splitted = re.split(self.HG_RELEASE_HEADER, cnt)

        i = 1  # on index==0 there is "Python News" header
        while True:
            if len(splitted) <= i:
                break
            header = splitted[i].strip()
            cnt = splitted[i+1].strip()

            version = item.version
            if item.version == '3.1.0':
                version = '3.1'

            if version in header:
                ver = extract_version(header)
                yield {
                    "version": ver,
                    # still better than docutils ReST parser
                    "notes": markdown(cnt),
                    "date": extract_date(header),
                    "url": item.url,
                }

            i += 2
