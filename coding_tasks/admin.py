from django.contrib import admin

from coding_tasks.models import Solution, Task

admin.site.register((Solution, Task))
