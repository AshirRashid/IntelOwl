# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

# Generated by Django 3.2.18 on 2023-03-07 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0019_mitm_configs'),
        ('visualizers_manager', '0005_visualizerconfig_disabled_in_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualizerreport',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visualizerreports', to='api_app.job'),
        ),
    ]
