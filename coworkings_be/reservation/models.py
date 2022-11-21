import decimal

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators
from django.db import models
from users.models import CustomUser
from utils.mixins import AuditMixin
from working_spaces.models import WorkingSpace


class Reservation(AuditMixin, models.Model):
    """
    model for reserve one place for specific time
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    working_space = models.ForeignKey(WorkingSpace, on_delete=models.CASCADE)
    datetime_range = DateTimeRangeField()
    paid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            ExclusionConstraint(
                name="exclude_overlap",
                expressions=[
                    ("datetime_range", RangeOperators.OVERLAPS),
                ],
            )
        ]

    def __str__(self):
        return f"{self.working_space} - {self.user}"

    @property
    def coworking(self):
        return self.working_space.coworking

    @property
    def start_time(self):
        return self.datetime_range.lower

    @property
    def end_time(self):
        return self.datetime_range.upper

    @property
    def duration(self):
        return self.end_time - self.start_time

    def total_price(self):
        return decimal.Decimal(
            int(self.working_space.base_price) * self.duration.seconds
        )
