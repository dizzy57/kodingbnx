import datetime
import os

import requests
from django.urls import reverse

from coding_tasks import task_schedule
from coding_tasks.models import Solution, Task

BOT_API_KEY = os.environ["TELEGRAM_BOT_API_KEY"]
CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])
URL_BASE = f"https://api.telegram.org/bot{BOT_API_KEY}/"

SITE_URL = "https://kodingbnx.pythonanywhere.com"
STAFF_USERS = "@asizikov @dizzy57"
NO_TASK_FOR_TODAY_MESSAGE = f"{STAFF_USERS} No task for today :("
NO_TASK_FOR_TOMORROW_MESSAGE = f"{STAFF_USERS} No task for tomorrow"


class TelegramApi:
    def __init__(self):
        self.session = requests.session()

    def close(self):
        self.session.close()

    def _call(self, endpoint, data):
        res = self.session.post(URL_BASE + endpoint, json=data)
        res.raise_for_status()
        return res.json()

    def send_message(self, text):
        data = {"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True}
        return self._call("sendMessage", data)

    def pin_message(self, message_id):
        data = {
            "chat_id": CHAT_ID,
            "message_id": message_id,
            "disable_notification": True,
        }
        return self._call("pinChatMessage", data)


class TelegramBot:
    def __init__(self):
        self.api = TelegramApi()
        self.today = task_schedule.today()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.api.close()
        return False

    def send_and_pin_task_for_today(self):
        try:
            task = Task.objects.get(date=self.today)
        except Task.DoesNotExist:
            self.api.send_message(NO_TASK_FOR_TODAY_MESSAGE)
            return

        m = self.api.send_message("\n".join((task.name, task.url, SITE_URL + "/")))
        self.api.pin_message(m["result"]["message_id"])

    def send_solutions_for_today(self):
        today_solutions_url = reverse("solutions_day", kwargs={"date": self.today})
        text = f"Solutions:\n{SITE_URL}{today_solutions_url}"
        self.api.send_message(text)

    def notify_if_no_tasks_for_tomorrow(self):
        tomorrow = self.today + datetime.timedelta(days=1)
        if not Task.objects.filter(date=tomorrow):
            self.api.send_message(NO_TASK_FOR_TOMORROW_MESSAGE)

    def notify_additional_solution(self, solution: Solution):
        today_solutions_url = reverse("solutions_day", kwargs={"date": self.today})
        text = f"New solution by {solution.user.get_short_name()} ({solution.language}): {SITE_URL}{today_solutions_url}#u{solution.user.id}"
        self.api.send_message(text)
