from constance import config
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView
from shapeshifter.views import MultiModelFormView

from coding_tasks.forms import (
    CreateUserAndSetShortNameForm,
    ProfileUpdateForm,
    SuggestionAddForm,
    UserUpdateForm,
)
from coding_tasks.models import Suggestion


class UserUpdateView(LoginRequiredMixin, MultiModelFormView):
    template_name = "coding_tasks/user.html"
    success_url = reverse_lazy("user")
    form_classes = [UserUpdateForm, ProfileUpdateForm]
    extra_context = {"suggestion_form": SuggestionAddForm()}

    def get_instances(self):
        user = self.request.user
        return {
            "userupdateform": user,
            "profileupdateform": user.profile,
        }


class SuggestionAddView(LoginRequiredMixin, RedirectView):
    pattern_name = "user"

    def post(self, request, *args, **kwargs):
        form = SuggestionAddForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            Suggestion.objects.update_or_create(
                url=url, defaults={"user": request.user}
            )
        return super().post(request, *args, **kwargs)


class SignUpView(CreateView):
    template_name = "coding_tasks/sign_up.html"
    success_url = reverse_lazy("login")
    form_class = CreateUserAndSetShortNameForm

    def dispatch(self, request, *args, **kwargs):
        if not config.ENABLE_SIGN_UP:
            return HttpResponseNotFound()
        return super().dispatch(request, *args, **kwargs)
