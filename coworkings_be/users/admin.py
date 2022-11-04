from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("role", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "nick_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "role", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "nick_name")
    list_filter = ("role", "date_joined")
    list_display = ("id", "email", "role", "nick_name", "date_joined", "is_active")
    ordering = ("date_joined",)
    list_per_page = 30
