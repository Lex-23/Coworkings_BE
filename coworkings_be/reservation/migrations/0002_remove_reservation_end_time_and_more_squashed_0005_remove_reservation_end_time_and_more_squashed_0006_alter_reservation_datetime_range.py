# Generated by Django 4.1.2 on 2022-11-21 13:17

import django.contrib.postgres.constraints
import django.contrib.postgres.fields.ranges
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservation", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reservation",
            name="end_time",
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="start_time",
        ),
        migrations.AddField(
            model_name="reservation",
            name="datetime_range",
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(
                default=None
            ),
        ),
        migrations.AddConstraint(
            model_name="reservation",
            constraint=django.contrib.postgres.constraints.ExclusionConstraint(
                expressions=[("datetime_range", "&&")], name="exclude_overlap"
            ),
        ),
        migrations.AddField(
            model_name="reservation",
            name="paid",
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name="reservation",
            name="total_price",
        ),
        migrations.AlterField(
            model_name="reservation",
            name="datetime_range",
            field=django.contrib.postgres.fields.ranges.DateTimeRangeField(),
        ),
    ]
