from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coding_tasks", "0005_switch_to_unique_constraint"),
    ]

    operations = [
        migrations.AlterField(
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
                    ("racket", "Racket"),
                    ("ruby", "Ruby"),
                    ("rust", "Rust"),
                    ("scala", "Scala"),
                    ("text", "Text only"),
                ],
                default="text",
                max_length=6,
            ),
        ),
        migrations.AddIndex(
            model_name="task",
            index=models.Index(fields=["url", "date"], name="coding_task_url_date_idx"),
        ),
    ]
