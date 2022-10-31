import os

from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser, UserRoles
from utils.mixins import AuditMixin

COWORKING_IMAGES_UPLOAD_DIR = os.environ["COWORKING_IMAGES_UPLOAD_DIR"]


class CoworkingStatus(models.IntegerChoices):
    VERIFIED = 1
    NOT_VERIFIED = 2
    TEMPORARILY_CLOSED = 3


class Coworking(models.Model, AuditMixin):
    """
    This model describes coworking
    Simple User(Guest) can not create a coworking
    """

    title = models.CharField(max_length=300)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=250, null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to=COWORKING_IMAGES_UPLOAD_DIR, blank=True, null=True
    )
    status = models.IntegerField(
        choices=CoworkingStatus.choices, default=CoworkingStatus.NOT_VERIFIED
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.owner.role == UserRoles.GUEST:
            raise ValidationError("Owner can not be a Guest")
        super(Coworking, self).save(*args, **kwargs)
