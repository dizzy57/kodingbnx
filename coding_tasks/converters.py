import datetime
import re


class DateConverter:
    regex = r"(\d{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])"

    def to_python(self, value: str) -> datetime.date:
        match = re.match(self.regex, value)
        ymd = map(int, match.groups())
        return datetime.date(*ymd)

    def to_url(self, value: datetime.date) -> str:
        return value.strftime("%Y-%m-%d")
