# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

# Generated by Django 3.2.18 on 2023-03-08 16:23

import django.db.models.deletion
from django.db import migrations, models


def migrate(apps, schema_editor):
    AnalyzerConfig = apps.get_model("analyzers_manager", "AnalyzerConfig")
    AnalyzerReport = apps.get_model("analyzers_manager", "AnalyzerReport")
    for report in AnalyzerReport.objects.all():
        report.config = AnalyzerConfig.objects.get(name=report.name)
        report.save()


def backwards_migrate(apps, schema_editor):
    AnalyzerReport = apps.get_model("analyzers_manager", "AnalyzerReport")
    for report in AnalyzerReport.objects.all():
        report.name = report.config.name
        report.save()


class Migration(migrations.Migration):

    dependencies = [
        ("api_app", "0019_mitm_configs"),
        ("analyzers_manager", "0007_alter_analyzerreport_job"),
    ]

    operations = [
        migrations.AddField(
            model_name="analyzerreport",
            name="config",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reports",
                to="analyzers_manager.analyzerconfig",
            ),
        ),
        migrations.AlterField(
            model_name="analyzerreport",
            name="name",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.RunPython(migrate, backwards_migrate),
        migrations.AlterField(
            model_name="analyzerreport",
            name="config",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reports",
                to="analyzers_manager.analyzerconfig",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="analyzerreport",
            unique_together={("config", "job")},
        ),
        migrations.RemoveField(
            model_name="analyzerreport",
            name="name",
        ),
    ]
