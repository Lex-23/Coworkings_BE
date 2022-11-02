from django.db import models
from users.models import CustomUser
from utils.fields import PriceField
from utils.mixins import AuditMixin
from working_spaces.models import WorkingSpace


class Reservation(AuditMixin, models.Model):
    """
    model for reserve one place for specific time
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    working_space = models.ForeignKey(WorkingSpace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = PriceField()

    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.working_space} - {self.user} - {self.total_price}"

    @property
    def coworking(self):
        return self.working_space.coworking
