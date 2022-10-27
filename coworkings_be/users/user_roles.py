from django.db import models


class UserRoles(models.TextChoices):
    GUEST = "guest"
    OWNER = "owner"
    ADMINISTRATOR = "administrator"
