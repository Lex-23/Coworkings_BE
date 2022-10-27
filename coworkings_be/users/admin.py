from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    fields = ("email", "role")
    list_display = ("id", "email", "role")
