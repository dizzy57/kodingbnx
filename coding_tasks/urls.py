from django.urls import path
from coding_tasks.views import SubmitView

urlpatterns = [path("", SubmitView.as_view(), name="submit")]
