import django.contrib.auth.views as auth_views
from django.urls import path

from coding_tasks.views import (
    EditTasksView,
    SignUpView,
    SolutionsView,
    SubmitView,
    UserUpdateView,
)

urlpatterns = [
    path("", SubmitView.as_view(), name="submit"),
    path("solutions", SolutionsView.as_view(), name="solutions"),
    path("user", UserUpdateView.as_view(), name="user"),
    path(
        "login",
        auth_views.LoginView.as_view(template_name="coding_tasks/login.html"),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "password_change",
        auth_views.PasswordChangeView.as_view(
            template_name="coding_tasks/password_change.html", success_url="user"
        ),
        name="password_change",
    ),
    path("sign_up", SignUpView.as_view(), name="sign_up"),
    path("edit_tasks", EditTasksView.as_view(), name="edit_tasks"),
]
