# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

# Generated by Django 3.2.16 on 2023-01-11 10:43

import django.core.validators
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
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "company_name",
                    models.CharField(
                        max_length=32,
                        validators=[django.core.validators.MinLengthValidator(3)],
                    ),
                ),
                (
                    "company_role",
                    models.CharField(
                        max_length=32,
                        validators=[django.core.validators.MinLengthValidator(3)],
                    ),
                ),
                (
                    "twitter_handle",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=16,
                        validators=[django.core.validators.MinLengthValidator(3)],
                    ),
                ),
                (
                    "discover_from",
                    models.CharField(
                        choices=[
                            (
                                "search_engine",
                                "Search Engine (Google, DuckDuckGo, etc.)",
                            ),
                            ("was_recommended", "Recommended by friend or colleague"),
                            ("social_media", "Social media"),
                            ("blog_or_publication", "Blog or Publication"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=32,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "User Profiles",
            },
        ),
    ]
