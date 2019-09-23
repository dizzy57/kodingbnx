from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from coding_tasks.models import Solution, Task


class SubmitView(UpdateView):
    template_name = "submit.html"
    success_url = reverse_lazy("solutions")
    model = Solution
    fields = ["url"]

    def get_object(self, queryset=None):
        task = Task.today()
        try:
            return Solution.objects.get(task=task, user=self.request.user)
        except Solution.DoesNotExist:
            return Solution(task=task, user=self.request.user)


class SolutionsView(TemplateView):
    template_name = "solutions.html"
