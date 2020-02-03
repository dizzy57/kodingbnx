from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Suggestion(models.Model):
    url = models.URLField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    submitted_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    away_until = models.DateField(blank=True, null=True)


@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
