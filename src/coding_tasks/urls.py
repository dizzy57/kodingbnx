import django.contrib.auth.views as auth_views
from constance import config
from django.urls import path, register_converter

from coding_tasks.converters import DateConverter
from coding_tasks.views.editor import EditTasksView, ResendNotificationView
from coding_tasks.views.solutions import SolutionsDayView, SolutionsWeekView, SubmitView
from coding_tasks.views.users import SignUpView, SuggestionAddView, UserUpdateView

register_converter(DateConverter, "date")

urlpatterns = [
    path("", SubmitView.as_view(), name="submit"),
    path("solutions", SolutionsWeekView.as_view(), name="solutions_week"),
    path("solutions/<date:date>", SolutionsDayView.as_view(), name="solutions_day"),
    # region User and auth
    path("user", UserUpdateView.as_view(), name="user"),
    path("suggest", SuggestionAddView.as_view(), name="suggest"),
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="coding_tasks/login.html",
            extra_context={"enable_sign_up": lambda: config.ENABLE_SIGN_UP},
        ),
        name="login",
    ),
    path("sign_up", SignUpView.as_view(), name="sign_up"),
    path("logout", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "password_change",
        auth_views.PasswordChangeView.as_view(
            template_name="coding_tasks/password_change.html", success_url="user"
        ),
        name="password_change",
    ),
    # endregion
    # region Task editor
    path("edit_tasks", EditTasksView.as_view(), name="edit_tasks"),
    path(
        "resend_notification",
        ResendNotificationView.as_view(),
        name="resend_notification",
    ),
    # endregion
]
