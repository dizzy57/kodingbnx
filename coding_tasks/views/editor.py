import datetime
import itertools
import json

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.middleware.csrf import get_token as get_csrf_token
from django.views import View
from django.views.generic import TemplateView

from coding_tasks import task_schedule
from coding_tasks.models import Task
from telegram_bot.telegram_api import TelegramBot

DATE_FORMAT = "%Y-%m-%d"


class EditTasksView(PermissionRequiredMixin, TemplateView):
    permission_required = "coding_tasks.edit_tasks"
    template_name = "coding_tasks/edit_tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        editor_data = {}

        start_date = task_schedule.today()
        editor_data["start_date"] = start_date.strftime(DATE_FORMAT)

        tasks_by_date = {
            task.date: {"name": task.name, "url": task.url}
            for task in (Task.objects.filter(date__gte=start_date))
        }

        max_date = max(tasks_by_date.keys(), default=datetime.date.min)
        dates = itertools.takewhile(
            lambda x: x <= max_date,
            (start_date + datetime.timedelta(days=n) for n in itertools.count()),
        )

        empty_task = {"name": "", "url": ""}
        tasks = [
            {"id": idx, **tasks_by_date.get(date, empty_task)}
            for idx, date in enumerate(dates)
        ]
        editor_data["next_id"] = len(tasks)

        editor_data["tasks"] = tasks
        editor_data["csrf_token"] = get_csrf_token(self.request)

        context["editor_data"] = editor_data
        context["debug"] = settings.DEBUG

        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        with transaction.atomic():
            date = datetime.datetime.strptime(data["start_date"], DATE_FORMAT).date()
            delete_dates = []
            for task in data["tasks"]:
                if task["name"] and task["url"]:
                    Task.objects.update_or_create(
                        date=date, defaults={"name": task["name"], "url": task["url"]}
                    )
                else:
                    delete_dates.append(date)
                date += datetime.timedelta(days=1)
            Task.objects.filter(Q(date__in=delete_dates) | Q(date__gte=date)).delete()
        return HttpResponse()


class ResendNotificationView(PermissionRequiredMixin, View):
    permission_required = "coding_tasks.edit_tasks"

    def post(self, request, *args, **kwargs):
        with TelegramBot() as bot:
            bot.send_and_pin_task_for_today()
        return HttpResponse()
