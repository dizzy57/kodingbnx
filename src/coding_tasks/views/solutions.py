import datetime
from collections import defaultdict

from constance import config
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Max, Q
from django.http import Http404
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, UpdateView
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from coding_tasks import task_schedule
from coding_tasks.models import Solution, Task
from telegram_bot.telegram_api import TelegramBot


def can_disclose_solutions_for_user(user: User):
    can_disclose_based_on_time = task_schedule.can_disclose_solutions()
    user_has_solution_today = config.ALLOW_SOLUTIONS_EARLY and bool(
        user.solution_set.filter(task__date=task_schedule.today())
    )
    return can_disclose_based_on_time or user_has_solution_today


class SubmitView(LoginRequiredMixin, UpdateView):
    template_name = "coding_tasks/submit.html"
    model = Solution
    fields = ["code", "language"]

    def get_object(self, queryset=None):
        today = task_schedule.today()
        user = self.request.user

        try:
            task = Task.objects.get(date=today)
        except Task.DoesNotExist:
            return None

        try:
            return Solution.objects.select_related("task").get(task=task, user=user)
        except Solution.DoesNotExist:
            new_solution = Solution(task=task, user=user)
            previous_solution = (
                Solution.objects.filter(user=user)
                .order_by("task__date")
                .only("language")
                .last()
            )
            if previous_solution:
                new_solution.language = previous_solution.language
            return new_solution

    def form_valid(self, form):
        res = super().form_valid(form)
        # Since we're already writing to the database, let's bump the session too
        # This will send a new cookie to the user
        self.request.session.modified = True

        if task_schedule.can_disclose_solutions():
            # We've got an additional solution after the deadline
            with TelegramBot() as bot:
                bot.notify_additional_solution(self.object)
        return res

    def get_success_url(self):
        if config.ALLOW_SOLUTIONS_EARLY:
            today = task_schedule.today()
            return reverse("solutions_day", args=[today])
        else:
            return reverse("solutions_week")


class SolutionsWeekView(LoginRequiredMixin, TemplateView):
    template_name = "coding_tasks/solutions_week.html"
    show_columns = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = task_schedule.today()
        all_days = [
            today - datetime.timedelta(days=x) for x in range(self.show_columns)
        ]
        context["all_days"] = all_days
        last_date = all_days[-1]

        solutions = Solution.objects.prefetch_related("user", "task").filter(
            task__date__lte=today, task__date__gte=last_date, user__is_active=True
        )

        tasks_by_day = {}
        solved_dates_by_user = defaultdict(set)
        for solution in solutions:
            tasks_by_day[solution.task.date] = solution.task
            solved_dates_by_user[solution.user].add(solution.task.date)
        context["days_and_tasks"] = [(day, tasks_by_day.get(day)) for day in all_days]

        users_and_solved_dates = list(solved_dates_by_user.items())
        users_and_solved_dates.sort(key=lambda x: x[0].get_short_name())
        context["users_and_solved_dates"] = users_and_solved_dates

        can_disclose_solutions = can_disclose_solutions_for_user(self.request.user)
        context["can_disclose_solutions"] = can_disclose_solutions

        users_without_recent_solutions = list(
            User.objects.filter(is_active=True)
            .annotate(last_solution=Max("solution__task__date"))
            .filter(Q(last_solution__lt=last_date) | Q(last_solution=None))
            .select_related("profile")
        )

        slackers = {
            user
            for user in users_without_recent_solutions
            if user.profile.away_until is None or user.profile.away_until <= today
        }

        slackers_and_last_seen_date = [
            (user.get_short_name(), self.last_seen_date(user)) for user in slackers
        ]
        slackers_and_last_seen_date.sort(key=lambda x: x[1] or datetime.date.min)
        context["slackers_and_last_seen_date"] = slackers_and_last_seen_date

        away_and_away_until_date = [
            (user.get_short_name(), user.profile.away_until)
            for user in users_without_recent_solutions
            if user not in slackers
        ]
        away_and_away_until_date.sort(key=lambda x: x[1])
        context["away_and_away_until_date"] = away_and_away_until_date

        return context

    @staticmethod
    def last_seen_date(user):
        dates = [user.last_solution, user.profile.away_until]
        non_none_dates = [x for x in dates if x is not None]
        return max(non_none_dates, default=None)


class SolutionsDayView(LoginRequiredMixin, DetailView):
    template_name = "coding_tasks/solutions_day.html"
    model = Task
    slug_url_kwarg = "date"
    slug_field = "date"

    def get_object(self, queryset=None):
        today = task_schedule.today()
        can_disclose_solutions = can_disclose_solutions_for_user(self.request.user)
        date = self.kwargs["date"]
        if date > today or (date == today and not can_disclose_solutions):
            raise Http404("Should not disclose tasks or solutions too early")

        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        formatter = HtmlFormatter()
        context["pygments_css"] = formatter.get_style_defs(".highlight")

        task: Task = self.object
        solutions = task.solution_set.select_related("user").order_by(
            "user__first_name"
        )

        solution_and_formatted = []
        for solution in solutions:
            lexer = get_lexer_by_name(solution.language, stripall=True)
            formatted_solution = highlight(solution.code, lexer, formatter)
            solution_and_formatted.append((solution, formatted_solution))
        context["solution_and_formatted"] = solution_and_formatted

        return context
