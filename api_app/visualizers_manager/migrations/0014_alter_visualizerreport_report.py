# Generated by Django 4.1.7 on 2023-05-02 10:43

from django.db import migrations, models

import api_app.visualizers_manager.validators


class Migration(migrations.Migration):

    dependencies = [
        ('visualizers_manager', '0013_params'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualizerreport',
            name='report',
            field=models.JSONField(default=list, validators=[api_app.visualizers_manager.validators.validate_report]),
        ),
    ]
