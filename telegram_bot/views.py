import datetime
import functools
import os

from django.http import HttpResponse

from coding_tasks import task_schedule
from coding_tasks.models import Solution, Task
from telegram_bot.telegram_api import TelegramApi

CRON_API_KEY = os.environ["CRON_API_KEY"]
SITE_URL = "https://kodingbnx.pythonanywhere.com/"
NO_TOMORROW_TASK_MESSAGE = "@asizikov @dizzy57 No task for tomorrow"


def check_api_key(f):
    @functools.wraps(f)
    def wrapped(request):
        key = request.GET.get("api_key")
        if key != CRON_API_KEY:
            return HttpResponse(status=403)
        f()
        return HttpResponse(status=204)

    return wrapped


@check_api_key
def morning_send_task():
    with TelegramApi() as api:
        today = task_schedule.today()
        try:
            task = Task.objects.get(date=today)
        except Task.DoesNotExist:
            api.send_message("No task for today :(")
            return

        m = api.send_message("\n".join((task.name, task.url, SITE_URL)))
        api.pin_message(m["result"]["message_id"])
        notify_if_no_task_for_tomorrow(api)


@check_api_key
def evening_send_solutions():
    today = task_schedule.today()
    solutions = list(
        Solution.objects.filter(task__date=today)
        .order_by("user__first_name")
        .select_related("user")
    )

    text = f"Solutions {today:%d/%m}:\n"
    if solutions:
        text += "\n".join(
            f"{solution.user.first_name} {solution.url}" for solution in solutions
        )
    else:
        text += "None"

    with TelegramApi() as api:
        api.send_message(text)
        notify_if_no_task_for_tomorrow(api)


def notify_if_no_task_for_tomorrow(api):
    tomorrow = task_schedule.today() + datetime.timedelta(days=1)
    if not Task.objects.filter(date=tomorrow):
        api.send_message(NO_TOMORROW_TASK_MESSAGE)
