# Generated by Django 4.1.9 on 2023-05-18 08:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectors_manager', '0015_params'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectorconfig',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator('^\\w+$', 'Your name should match the [A-Za-z0-9_] characters')]),
        ),
    ]
