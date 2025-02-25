# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

# Generated by Django 3.2.18 on 2023-03-06 15:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0017_delete_organizationpluginstate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', 'Hex color')]),
        ),
        migrations.AlterField(
            model_name='tag',
            name='label',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]
