from django.contrib import admin

from coding_tasks.models import Solution, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "date"]
    ordering = ["date"]
    list_filter = ["date"]


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ["user", "task", "url"]
