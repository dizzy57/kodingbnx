from django.contrib import admin

from coding_tasks.models import Profile, Solution, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "date"]
    ordering = ["-date"]
    list_filter = ["date"]


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ["task", "user", "language"]
    ordering = ["-submitted_at"]
    list_filter = ["task__date"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "away_until"]
