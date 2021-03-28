from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coding_tasks", "0004_add_profiles_and_suggestions"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="solution",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="solution",
            constraint=models.UniqueConstraint(
                fields=("user", "task"), name="one_solution_per_user"
            ),
        ),
    ]
