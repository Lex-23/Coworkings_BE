from django.db import models
from users.models import CustomUser
from utils.fields import PriceField
from utils.mixins import AuditMixin
from working_spaces.models import WorkingSpace


class Reservation(models.Model, AuditMixin):
    """
    model for reserve one place for specific time
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    working_spaces = models.ForeignKey(WorkingSpace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = PriceField()

    def __str__(self):
        return f"{self.working_spaces} - {self.user} - {self.total_price}"