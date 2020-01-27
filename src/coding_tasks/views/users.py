from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from coding_tasks.forms import CreateUserAndSetShortNameForm


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
    form_class = CreateUserAndSetShortNameForm
