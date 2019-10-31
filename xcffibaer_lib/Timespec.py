from datetime import datetime
import locale

from dateutil.tz import gettz


DEFAULT_TZ = gettz()
DEFAULT_LOCALE = locale.getlocale()


class Timespec:
    def __init__(self, tag, format, timezone=DEFAULT_TZ, locale=DEFAULT_LOCALE):
        self.tag = tag
        self.format = format
        self.timezone = timezone
        self.locale = locale

    def render(self):
        if self.locale != DEFAULT_LOCALE:
            locale.setlocale(locale.LC_ALL, self.locale)

        result = datetime.now(self.timezone).strftime(self.format)

        if self.locale != DEFAULT_LOCALE:
            locale.setlocale(locale.LC_ALL, DEFAULT_LOCALE)

        return result

