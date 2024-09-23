# Generated by Django 5.1.1 on 2024-09-23 09:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users_app", "0003_blockeduser_friendrequest"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserActivity",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user_activity_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "activity_type",
                    models.CharField(
                        choices=[
                            ("friend_request_sent", "friend_request_sent"),
                            ("friend_request_accepted", "friend_request_accepted"),
                            ("friend_request_rejected", "friend_request_rejected"),
                        ],
                        max_length=50,
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("details", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_activity_user_model_manager",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
