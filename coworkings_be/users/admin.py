from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "email",
        "role",
        "first_name",
        "last_name",
        "nick_name",
        "date_joined",
        "is_active",
    )
    search_fields = ("email", "nick_name")
    list_filter = ("role", "date_joined")
    list_display = ("id", "email", "role", "nick_name", "date_joined", "is_active")
    ordering = ("date_joined",)
    list_per_page = 30
