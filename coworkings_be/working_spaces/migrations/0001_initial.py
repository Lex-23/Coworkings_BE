# Generated by Django 4.1.2 on 2022-10-31 14:00

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
import utils.fields
import utils.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("coworking", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TypeWorkingSpace",
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
                    "type",
                    models.IntegerField(
                        choices=[(1, "Simple"), (2, "Conference"), (3, "Vip")],
                        default=1,
                    ),
                ),
                ("label", models.CharField(default="A", max_length=5)),
                (
                    "base_price",
                    utils.fields.PriceField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                (
                    "coworking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coworking.coworking",
                    ),
                ),
            ],
            options={
                "unique_together": {("coworking", "type", "label")},
            },
        ),
        migrations.CreateModel(
            name="WorkingSpace",
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
                ("local_number", models.IntegerField(auto_created=True)),
                (
                    "coworking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="working_spaces",
                        to="working_spaces.typeworkingspace",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="working_spaces.typeworkingspace",
                    ),
                ),
            ],
            options={
                "unique_together": {("type", "local_number")},
            },
            bases=(models.Model, utils.mixins.AuditMixin),
        ),
    ]
