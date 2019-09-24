from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.date:%d-%m} {self.name}"


class Solution(models.Model):
    class Meta:
        unique_together = ["task", "user"]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    url = models.URLField(max_length=255, verbose_name="URL")
    submitted_at = models.DateTimeField(auto_now=True)
