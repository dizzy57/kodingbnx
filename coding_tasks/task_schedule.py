import datetime

import pytz

TZ = pytz.timezone("Europe/Amsterdam")


def today():
    now = datetime.datetime.now(TZ)
    date = now.date()
    return date
