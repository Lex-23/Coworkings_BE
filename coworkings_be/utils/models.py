from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from utils.mixins import AuditMixin


def validate_hashtag(value: str):
    if value[0] != "#":
        raise ValidationError("hashtag must be start from '#' symbol")
    elif value == "#":
        raise ValidationError("hashtag must contain minimum 1 symbol after '#'")
    elif not value[1:].isalnum():
        raise ValidationError(
            "hashtag must contain only alphanumerical symbols after '#'"
        )


class HashTag(AuditMixin, models.Model):
    title = models.CharField(max_length=250, unique=True, validators=[validate_hashtag])

    def __str__(self):
        return self.title


class BaseImages(AuditMixin, models.Model):
    """
    Base model for describing uploaded to gallery images
    """

    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    altText = models.TextField(null=True, blank=True)
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    hashtags = models.ManyToManyField(HashTag, blank=True)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"uniqueId: {self.uniqueId}, slug: {self.slug}"

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split("-")[4]
            self.slug = slugify(f"{self.title} {self.uniqueId}")
        super().save(*args, **kwargs)
