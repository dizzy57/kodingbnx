from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.date:%d/%m} {self.name}"


class Solution(models.Model):
    class Meta:
        unique_together = ["task", "user"]

    class SolutionLanguage(models.TextChoices):
        C = "c", "C"
        CPP = "cpp", "C++"
        CSHARP = "csharp", "C#"
        GO = "go", "Go"
        JAVA = "java", "Java"
        JAVASCRIPT = "js", "JavaScript"
        KOTLIN = "kotlin", "Kotlin"
        PYTHON = "python", "Python"
        RUBY = "ruby", "Ruby"
        RUST = "rust", "Rust"
        SCALA = "scala", "Scala"
        TEXT = "text", "Text only"

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    code = models.TextField()
    language = models.CharField(
        max_length=6, choices=SolutionLanguage.choices, default=SolutionLanguage.TEXT
    )
    submitted_at = models.DateTimeField(auto_now=True)
