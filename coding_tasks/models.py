import datetime

import pytz
from django.contrib.auth.models import User
from django.db import models

TZ = pytz.timezone("Europe/Amsterdam")


class Task(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.date:%d-%m} {self.name}"

    @classmethod
    def today(cls, date=None):
        if date is None:
            now = datetime.datetime.now(TZ)
            date = now.date()
        try:
            return cls.objects.get(date=date)
        except cls.DoesNotExist:
            return None


class Solution(models.Model):
    class Meta:
        unique_together = ["task", "user"]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    url = models.URLField(max_length=255)
    submitted_at = models.DateTimeField(auto_now=True)
