import re
from datetime import date

MONTHS = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 9,
    "aug": 9,
    "september": 9,
    "sep": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}

DATE_MAP = {
    "(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})": lambda m: date(*map(int, m)),
    "(\d{2})[-\/]([a-zA-Z]{3,})[-\/](\d{4})":
        lambda m: date(int(m[2]), MONTHS[m[1].lower()], int(m[0])),
    "([a-zA-z]+) (\d{1,2}), (\d{4})":
        lambda m: date(int(m[2]), MONTHS[m[0].lower()], int(m[1])),
}


def extract_version(text):
    if not isinstance(text, str):
        raise ValueError("Parameter must be `str` type")

    matches = re.search("(\d+(\.\d+)?(\.\d+)?([a-zA-Z0-9 ]*)?)", text)

    if matches and matches.groups():
        return matches.groups()[0].strip()

    return None


def extract_date(text):
    for regexp, callback in DATE_MAP.items():
        matches = re.search(regexp, text)
        if matches:
            return callback(matches.groups())

    return None
