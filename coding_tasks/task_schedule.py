import datetime

import pytz

TZ = pytz.timezone("Europe/Amsterdam")
NEW_TASK_TIME = datetime.time(hour=6)
SOLUTIONS_TIME = datetime.time(hour=17)


def today(now=None):
    if now is None:
        now = datetime.datetime.now(TZ)
    if now.time() >= NEW_TASK_TIME:
        return now.date()
    else:
        return now.date() - datetime.timedelta(days=1)


def should_disclose_solutions(now=None):
    if now is None:
        now = datetime.datetime.now(TZ)
    return not (NEW_TASK_TIME < now.time() < SOLUTIONS_TIME)
