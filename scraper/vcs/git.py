import re

import requests
from markdown import markdown

from modules.utils.classes import BaseScrapper
from modules.utils.functions import extract_version, extract_date


class Scrapper(BaseScrapper):
    project_name = "GIT"

    base_url = "https://raw.githubusercontent.com/git/git/master/" \
               "Documentation/RelNotes/{}"
    tags_url = "https://api.github.com/repos/git/git/tags"
    git_trees = "https://api.github.com/repos/git/" \
                "git/git/trees/master?recursive=1"
    header_regexp = "(GIT.*Release Notes\n=+\n\n)"

    _tags = None

    @property
    def tags(self):
        if self._tags is None:
            tags = requests.get(self.tags_url).json()

            self._tags = {
                extract_version(tag["name"]): tag["commit"]["url"]
                for tag in tags
            }

        return self._tags

    def _notes_tree(self, data):
        for tree in data["tree"]:
            if tree["path"] == "Documentation/RelNotes":
                return tree["url"]

    def get_notes_urls(self):
        resp = requests.get(self.git_trees)

        notes_tree_url = self._notes_tree(resp.json())
        resp = requests.get(notes_tree_url)
        for entry in resp.json()['tree']:
            yield self.base_url.format(entry["path"])

    def get_date(self, version):
        tag_commit_url = self.tags.get(version)

        if not tag_commit_url:
            return None

        commit = requests.get(tag_commit_url).json()
        return extract_date(commit["commit"]["author"]["date"])

    def initial(self):
        notes_urls = self.get_notes_urls()

        for note_url in notes_urls:
            cnt = requests.get(note_url).content.decode()
            _, header, cnt = re.split(self.header_regexp, cnt, 0, re.I)
            version = extract_version(header.replace(" Release Notes", ""))

            yield {
                "version": version,
                "notes": markdown(cnt),
                "date": self.get_date(version),
                "url": note_url,
            }
