from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coding_tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solution", name="url", field=models.TextField()
        ),
        migrations.RenameField(model_name="solution", old_name="url", new_name="code"),
        migrations.AddField(
            model_name="solution",
            name="language",
            field=models.CharField(
                choices=[
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
                ],
                default="text",
                max_length=6,
            ),
        ),
    ]
