# Generated by Django 5.1.1 on 2024-09-23 10:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "notification_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("friend_request_sent", "friend_request_sent"),
                            ("friend_request_accepted", "friend_request_accepted"),
                        ],
                        max_length=100,
                    ),
                ),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                (
                    "from_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification_from_user_model_manager",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "to_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification_to_user_model_manager",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
