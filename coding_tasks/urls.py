import os

import django.contrib.auth.views as auth_views
from django.urls import path

from coding_tasks.views import (
    EditTasksView,
    ResendNotificationView,
    SignUpView,
    SolutionsView,
    SubmitView,
    UserUpdateView,
)

ENABLE_SIGN_UP = os.environ["ENABLE_SIGN_UP"] == "1"

urlpatterns = [
    path("", SubmitView.as_view(), name="submit"),
    path("solutions", SolutionsView.as_view(), name="solutions"),
    path("user", UserUpdateView.as_view(), name="user"),
    # region Auth
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="coding_tasks/login.html",
            extra_context={"enable_sign_up": ENABLE_SIGN_UP},
        ),
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
    # endregion
    # region Task admin
    path("edit_tasks", EditTasksView.as_view(), name="edit_tasks"),
    path(
        "resend_notification",
        ResendNotificationView.as_view(),
        name="resend_notification",
    ),
    # endregion
]

if ENABLE_SIGN_UP:
    urlpatterns.append(path("sign_up", SignUpView.as_view(), name="sign_up"))
