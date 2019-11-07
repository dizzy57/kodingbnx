import functools
import os

from django.http import HttpResponse

from telegram_bot.telegram_api import TelegramBot

CRON_API_KEY = os.environ["CRON_API_KEY"]


def cronjob_api_call(f):
    @functools.wraps(f)
    def wrapped(request):
        key = request.GET.get("api_key")
        if key != CRON_API_KEY:
            return HttpResponse(status=403)
        f()
        return HttpResponse(status=204)

    return wrapped


@cronjob_api_call
def morning_send_task():
    with TelegramBot() as bot:
        bot.send_and_pin_task_for_today()
        bot.notify_if_no_tasks_for_tomorrow()
        bot.notify_if_first_day_of_month()


@cronjob_api_call
def evening_send_solutions():
    with TelegramBot() as bot:
        bot.send_solutions_for_today()
        bot.notify_if_no_tasks_for_tomorrow()
