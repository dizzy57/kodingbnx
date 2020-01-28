from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from shapeshifter.views import MultiModelFormView

from coding_tasks.forms import (
    CreateUserAndSetShortNameForm,
    ProfileUpdateForm,
    UserUpdateForm,
)


class UserUpdateView(LoginRequiredMixin, MultiModelFormView):
    template_name = "coding_tasks/user.html"
    success_url = reverse_lazy("user")
    form_classes = [UserUpdateForm, ProfileUpdateForm]

    def get_instances(self):
        user = self.request.user
        return {
            "userupdateform": user,
            "profileupdateform": user.profile,
        }


class SignUpView(CreateView):
    template_name = "coding_tasks/sign_up.html"
    success_url = reverse_lazy("login")
    form_class = CreateUserAndSetShortNameForm
