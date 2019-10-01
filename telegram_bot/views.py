import os
from functools import wraps

from django.http import HttpResponse

from coding_tasks import task_schedule
from coding_tasks.models import Solution, Task
from telegram_bot.telegram_api import pin_message, send_message

CRON_API_KEY = os.environ["CRON_API_KEY"]


def check_api_key(f):
    @wraps(f)
    def wrapped(request):
        key = request.GET.get("api_key")
        if key != CRON_API_KEY:
            return HttpResponse(status=403)
        f()
        return HttpResponse(status=204)

    return wrapped


@check_api_key
def morning_send_task():
    today = task_schedule.today()
    try:
        task = Task.objects.get(date=today)
    except Task.DoesNotExist:
        send_message("No task for today :(")
        return

    submit_url = "https://kodingbnx.bnx/"

    m = send_message("\n".join((task.name, task.url, submit_url)))
    pin_message(m["result"]["message_id"])


@check_api_key
def evening_send_solutions():
    today = task_schedule.today()
    solutions = (
        Solution.objects.filter(task__date=today)
        .order_by("user__first_name")
        .select_related("user")
    )

    text = f"Solutions {today:%d/%m}:\n"
    text += "\n".join(
        f"{solution.user.first_name} {solution.url}" for solution in solutions
    )
    send_message(text)
