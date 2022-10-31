from coworking.models import Coworking
from django.db import models
from utils.fields import PriceField
from utils.mixins import AuditMixin


class Type(models.IntegerChoices):
    SIMPLE = 1
    CONFERENCE = 2
    VIP = 3


class TypeWorkingSpace(models.Model):
    """
    model for create type of working space in specific coworking with base price
    One coworking must have unique scope: "coworking", "type", "label"
    Label - specific id for type of working space
    """

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
    coworking = models.ForeignKey(
        TypeWorkingSpace, on_delete=models.CASCADE, related_name="working_spaces"
    )

    class Meta:
        unique_together = ("type", "local_number")

    def __str__(self):
        return f"{self.local_number}{self.type.label}"
