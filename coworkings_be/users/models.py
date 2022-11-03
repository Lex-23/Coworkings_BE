from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import CustomUserManager


class UserRoles(models.IntegerChoices):
    GUEST = 1
    OWNER = 2
    ADMINISTRATOR = 3


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    avatar = models.ImageField(
        blank=True, null=True, upload_to=settings.USER_IMAGE_UPLOAD_DIR
    )
    nick_name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    role = models.IntegerField(choices=UserRoles.choices, default=UserRoles.GUEST)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} {self.nick_name if self.nick_name else ""}'
