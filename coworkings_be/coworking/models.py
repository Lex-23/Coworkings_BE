from django.conf import settings
from django.db import models
from users.models import CustomUser
from utils.mixins import AuditMixin
from utils.models import BaseImages


class CoworkingStatus(models.IntegerChoices):
    VERIFIED = 1
    NOT_VERIFIED = 2
    TEMPORARILY_CLOSED = 3


class Coworking(AuditMixin, models.Model):
    """
    This model describes coworking
    Simple User(Guest) can not create a coworking
    """

    title = models.CharField(max_length=300, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=250, null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to=settings.COWORKING_IMAGES_UPLOAD_DIR, blank=True, null=True
    )
    status = models.IntegerField(
        choices=CoworkingStatus.choices, default=CoworkingStatus.NOT_VERIFIED
    )

    class Meta:
        unique_together = ("title", "city")

    def __str__(self):
        return self.title

    @property
    def photos(self):
        return self.coworking_photo.all()


class CoworkingPhoto(BaseImages):
    """
    model for uploaded images to Coworking gallery
    """

    coworking = models.ForeignKey(
        Coworking, on_delete=models.CASCADE, related_name="coworking_photo"
    )
    image = models.ImageField(upload_to=settings.COWORKING_IMAGES_UPLOAD_DIR)
