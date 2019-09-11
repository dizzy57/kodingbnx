from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from coding_tasks.forms import SubmitSolutionForm
from coding_tasks.models import Solution, Task


class SubmitView(FormView):
    template_name = "submit.html"
    form_class = SubmitSolutionForm
    success_url = reverse_lazy("solutions")

    def form_valid(self, form):
        task = Task.today()
        if task:
            Solution.objects.get_or_create(
                task=task, user=self.request.user, defaults={"url": form.url}
            )
        return super().form_valid(form)


class SolutionsView(TemplateView):
    template_name = "solutions.html"
