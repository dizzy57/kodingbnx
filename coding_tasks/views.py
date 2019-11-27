import datetime
import itertools
import json
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Max, Q
from django.http import HttpResponse
from django.middleware.csrf import get_token as get_csrf_token
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, View

from coding_tasks import task_schedule
from coding_tasks.models import Solution, Task
from telegram_bot.telegram_api import TelegramBot

DATE_FORMAT = "%Y-%m-%d"


class SubmitView(LoginRequiredMixin, UpdateView):
    template_name = "coding_tasks/submit.html"
    success_url = reverse_lazy("solutions_week")
    model = Solution
    fields = ["code", "language"]

    def get_object(self, queryset=None):
        today = task_schedule.today()

        try:
            task = Task.objects.get(date=today)
        except Task.DoesNotExist:
            return None

        try:
            return Solution.objects.select_related("task").get(
                task=task, user=self.request.user
            )
        except Solution.DoesNotExist:
            return Solution(task=task, user=self.request.user)

    def form_valid(self, form):
        res = super().form_valid(form)
        if task_schedule.can_disclose_solutions():
            # We've got an additional solution after the deadline
            with TelegramBot() as bot:
                bot.notify_additional_solution(self.object)
        return res


class SolutionsWeekView(LoginRequiredMixin, TemplateView):
    template_name = "coding_tasks/solutions_week.html"
    SHOW_COLUMNS = 7

    def get_context_data(self, **context):
        today = task_schedule.today()
        all_days = [
            today - datetime.timedelta(days=x) for x in range(self.SHOW_COLUMNS)
        ]
        context["all_days"] = all_days
        last_date = all_days[-1]

        solutions = Solution.objects.prefetch_related("user", "task").filter(
            task__date__lte=today, task__date__gte=last_date
        )

        solved_dates_by_user = defaultdict(set)
        for solution in solutions:
            solved_dates_by_user[solution.user].add(solution.task.date)

        users_and_solved_dates = list(solved_dates_by_user.items())
        users_and_solved_dates.sort(key=lambda x: x[0].get_short_name())
        context["users_and_solved_dates"] = users_and_solved_dates

        can_disclose_solutions = task_schedule.can_disclose_solutions()
        context["can_disclose_solutions"] = can_disclose_solutions

        users_without_recent_solutions = (
            User.objects.filter(is_active=True)
            .annotate(last_solution=Max("solution__task__date"))
            .filter(Q(last_solution__lt=last_date) | Q(last_solution=None))
            .order_by("last_solution")
        )
        slackers = [
            (user.get_short_name() or user.username, user.last_solution)
            for user in users_without_recent_solutions
        ]
        context["slackers"] = slackers

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "coding_tasks/user.html"
    success_url = reverse_lazy("user")
    model = User
    fields = ["first_name"]

    def get_object(self, queryset=None):
        return self.request.user


class SignUpView(CreateView):
    template_name = "coding_tasks/sign_up.html"
    success_url = reverse_lazy("login")
    form_class = UserCreationForm


class EditTasksView(PermissionRequiredMixin, TemplateView):
    permission_required = "coding_tasks.edit_tasks"
    template_name = "coding_tasks/edit_tasks.html"

    def get_context_data(self, **kwargs):
        context = {}

        start_date = task_schedule.today()
        context["start_date"] = start_date.strftime(DATE_FORMAT)

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
        context["next_id"] = len(tasks)

        context["tasks"] = json.dumps(tasks)
        context["csrf_token"] = get_csrf_token(self.request)
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
