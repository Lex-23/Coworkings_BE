# Generated by Django 4.1.2 on 2022-11-02 16:20

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
import utils.fields
import utils.mixins
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("working_spaces", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
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
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                (
                    "total_price",
                    utils.fields.PriceField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "working_space",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="working_spaces.workingspace",
                    ),
                ),
            ],
            bases=(utils.mixins.AuditMixin, models.Model),
        ),
    ]
