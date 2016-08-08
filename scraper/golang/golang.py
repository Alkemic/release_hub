import scrapper

from modules.utils.functions import extract_version, extract_date


class ReleaseEntry(scrapper.CrawlerItem):
    version = scrapper.CrawlerField(
        "h2", lambda value, _, __: extract_version(value),
    )
    date = scrapper.CrawlerField(
        "h2", lambda value, _, __: extract_date(value),
    )


class ReleaseEntryCollection(scrapper.CrawlerMultiItem):
    item_class = ReleaseEntry
    content_selector = "#page .container h2"


def allowed_tags(tag):
    print(tag.attrs.get("id"))
    return not (
        str(tag.name) in ("h1", "style") or
        tag.attrs.get("id") == "footer"
    )


def filter_notes(value, content, response):
    tags = []

    for el in value.children:
        if hasattr(el, "tag") and allowed_tags(el):
            tags.append(str(el))

    return "".join(tags).replace(
        "<a href=\"/",
        "<a href=\"https://golang.org/",
    )


class ReleaseNote(scrapper.CrawlerItem):
    notes = scrapper.CrawlerField("#page .container", filter_notes, True)


class Scrapper():
    DOCS_URL = "https://golang.org/doc/go{}"
    RELEASE_NOTES_URL = "https://golang.org/doc/devel/release.html"

    def initial(self):
        for note in ReleaseEntryCollection(self.RELEASE_NOTES_URL):
            if note.version is None and note.date is None:
                continue

            notes = note.as_dict()

            notes_url = self.DOCS_URL.format(note.version)

            rn = ReleaseNote(notes_url)

            notes["notes"] = rn.notes
            notes["url"] = notes_url

            yield notes
