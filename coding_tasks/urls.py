from django.urls import path

from coding_tasks.views import SolutionsView, SubmitView, UserUpdateView

urlpatterns = [
    path("", SubmitView.as_view(), name="submit"),
    path("solutions", SolutionsView.as_view(), name="solutions"),
    path("user", UserUpdateView.as_view(), name="user"),
]
