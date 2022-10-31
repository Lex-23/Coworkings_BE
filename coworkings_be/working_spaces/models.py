from coworking.models import Coworking
from django.db import models
from utils.fields import PriceField
from utils.mixins import AuditMixin


class Type(models.IntegerChoices):
    SIMPLE = 1
    CONFERENCE = 2
    VIP = 3


class TypeWorkingSpace(models.Model):
    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)
    type = models.IntegerField(choices=Type.choices, default=Type.SIMPLE)
    label = models.CharField(max_length=5, default="A")
    base_price = PriceField()

    class Meta:
        unique_together = ("coworking", "type", "label")

    def __str__(self):
        return f"{self.coworking}, {self.type}, {self.base_price}"


class WorkingSpace(models.Model, AuditMixin):
    type = models.ForeignKey(TypeWorkingSpace, on_delete=models.CASCADE)
    local_number = models.IntegerField(auto_created=True)
    coworking = models.ForeignKey(TypeWorkingSpace, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.local_number}{self.type.label}"
