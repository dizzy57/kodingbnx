import os

from django.db import migrations

DB_NAME = os.environ["MYSQL_DATABASE"]


class Migration(migrations.Migration):
    dependencies = [
        ("coding_tasks", "0002_pastebin"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                f"ALTER DATABASE {DB_NAME} CHARACTER SET = utf8mb4 COLLATE utf8mb4_unicode_ci",
                "ALTER TABLE coding_tasks_task CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
                "ALTER TABLE coding_tasks_solution CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
                "ALTER TABLE coding_tasks_task MODIFY name VARCHAR(255) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL",
                "ALTER TABLE coding_tasks_task MODIFY url VARCHAR(255) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL",
                "ALTER TABLE coding_tasks_solution MODIFY code LONGTEXT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL",
                "ALTER TABLE coding_tasks_solution MODIFY language VARCHAR(6) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL",
                "ALTER TABLE django_admin_log CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci",
                "ALTER TABLE django_admin_log MODIFY object_repr VARCHAR(200) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL",
            ],
        )
    ]
