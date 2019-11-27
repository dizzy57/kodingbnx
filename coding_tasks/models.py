from django.contrib.auth.models import User
from django.db import models

SOLUTION_LANGUAGE_CHOICES = [
    ("c", "C"),
    ("cpp", "C++"),
    ("csharp", "C#"),
    ("go", "Go"),
    ("java", "Java"),
    ("js", "JavaScript"),
    ("kotlin", "Kotlin"),
    ("python", "Python"),
    ("ruby", "Ruby"),
    ("rust", "Rust"),
    ("scala", "Scala"),
    ("text", "Text only"),
]


class Task(models.Model):
    class Meta:
        permissions = [("edit_tasks", "Can edit task list")]

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
    code = models.TextField()
    language = models.CharField(
        max_length=6, choices=SOLUTION_LANGUAGE_CHOICES, default="text"
    )
    submitted_at = models.DateTimeField(auto_now=True)
