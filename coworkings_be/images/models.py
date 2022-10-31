from uuid import uuid4

from coworking.models import COWORKING_IMAGES_UPLOAD_DIR, Coworking
from django.db import models
from django.utils.text import slugify
from utils.mixins import AuditMixin


class BaseImages(models.Model, AuditMixin):
    """
    Base model for describing uploaded to gallery images
    """

    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    altText = models.TextField(null=True, blank=True)
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    hashtags = models.CharField(null=True, blank=True, max_length=300)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title}-{self.last_updated}"

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split("-")[4]
            self.slug = slugify(f"{self.title} {self.uniqueId}")


class CoworkingPhoto(BaseImages):
    """
    model for uploaded images to Coworking gallery
    """

    coworking = models.ForeignKey(Coworking, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=COWORKING_IMAGES_UPLOAD_DIR, blank=True, null=True
    )
