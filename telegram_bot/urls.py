from django.urls import path

from telegram_bot import views

urlpatterns = [
    path("morning_send_task", views.morning_send_task),
    path("evening_send_solutions", views.evening_send_solutions),
]
