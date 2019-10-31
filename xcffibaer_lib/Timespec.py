'''Helper class for rendering timestamps.

'''
from datetime import datetime
from locale import getlocale, setlocale, LC_ALL

from dateutil.tz import gettz


DEFAULT_TZ = gettz()
DEFAULT_LOCALE = getlocale()


class Timespec:
    def __init__(self, tag, format_, timezone=DEFAULT_TZ, locale=DEFAULT_LOCALE):
        self.tag = tag
        self.format = format_
        self.timezone = timezone
        self.locale = locale

    def render(self):
        if self.locale != DEFAULT_LOCALE:
            setlocale(LC_ALL, self.locale)

        result = datetime.now(self.timezone).strftime(self.format)

        if self.locale != DEFAULT_LOCALE:
            setlocale(LC_ALL, DEFAULT_LOCALE)

        return result
