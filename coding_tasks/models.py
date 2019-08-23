from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    date = models.DateField(editable=False, unique=True)


class Solution(models.Model):
    class Meta:
        unique_together = ["task", "user"]

    task = models.ForeignKey(Task, editable=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, editable=False, on_delete=models.PROTECT)
    url = models.URLField(max_length=255)
