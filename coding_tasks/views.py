from collections import defaultdict
from datetime import timedelta

from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from coding_tasks import task_schedule
from coding_tasks.models import Solution, Task


class SubmitView(UpdateView):
    template_name = "coding_tasks/submit.html"
    success_url = reverse_lazy("solutions")
    model = Solution
    fields = ["url"]

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


class SolutionsView(TemplateView):
    template_name = "coding_tasks/solutions.html"
    SHOW_COLUMNS = 7

    def get_context_data(self, **kwargs):
        context = {}

        today = task_schedule.today()
        all_days = [today - timedelta(days=x) for x in range(self.SHOW_COLUMNS)]
        last_date = all_days[-1]
        context["all_days"] = all_days

        solutions = Solution.objects.prefetch_related("user", "task").filter(
            task__date__lte=today, task__date__gte=last_date
        )
        per_user_solutions = defaultdict(dict)
        for solution in solutions:
            if (
                solution.task.date == today
                and not task_schedule.should_disclose_solutions()
            ):
                solution.url = None
            per_user_solutions[solution.user][solution.task.date] = solution

        current_user = self.request.user
        table_rows = [
            (
                user.username,
                user == current_user,
                [solutions.get(day) for day in all_days],
            )
            for user, solutions in per_user_solutions.items()
        ]
        table_rows.sort(key=lambda x: x[0])
        context["table_rows"] = table_rows

        return context
