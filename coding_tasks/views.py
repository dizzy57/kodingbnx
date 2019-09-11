from django.views.generic import TemplateView, FormView

from coding_tasks.forms import SubmitSolutionForm


class SubmitView(FormView):
    template_name = "submit.html"
    form_class = SubmitSolutionForm
    success_url = "/solutions"

    def form_valid(self, form):
        user = self.request.user
        task = ...  # Tasks.today
        return super().form_valid(form)


class SolutionsView(TemplateView):
    template_name = "solutions.html"
