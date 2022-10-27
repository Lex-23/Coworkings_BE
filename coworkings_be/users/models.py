import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager

IMAGE_UPLOAD_DIR = os.environ["IMAGE_UPLOAD_DIR"]


class UserRoles(models.TextChoices):
    GUEST = "guest"
    OWNER = "owner"
    ADMINISTRATOR = "administrator"


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=IMAGE_UPLOAD_DIR)
    nick_name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    company_name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    role = models.CharField(
        max_length=30, choices=UserRoles.choices, default=UserRoles.GUEST
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
