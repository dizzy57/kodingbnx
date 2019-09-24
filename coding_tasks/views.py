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
