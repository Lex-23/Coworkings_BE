from coworking.models import Coworking, CoworkingPhoto
from django.contrib import admin
from utils.models import HashTag
from working_spaces.admin import TypeWorkingSpaceInline, WorkingSpaceInline


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    list_display = ("title", "id")
    list_per_page = 30


@admin.register(CoworkingPhoto)
class CoworkingPhotoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("image", "title", "coworking")}),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("description", "altText", "uniqueId", "hashtags", "slug"),
            },
        ),
    )
    list_display = ("id", "uniqueId", "title", "coworking")
    search_fields = ("uniqueId",)
    list_filter = ("coworking",)
    readonly_fields = ["coworking"]

    def has_add_permission(self, request, obj=None):
        return False


class CoworkingPhotoInline(admin.TabularInline):
    model = CoworkingPhoto
    fields = ("image", "title")
    extra = 1


@admin.register(Coworking)
class CoworkingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("title", "owner", "city", "status")}),
        (
            "Working hours",
            {"classes": ("collapse",), "fields": ("opening_time", "closing_time")},
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("description", "address", "avatar"),
            },
        ),
    )
    search_fields = ("title", "city", "owner__email")
    list_filter = ("status",)
    list_display = (
        "id",
        "title",
        "owner",
        "city",
        "opening_time",
        "closing_time",
        "status",
    )
    ordering = ("status", "city")
    list_editable = ("status",)
    list_per_page = 30
    inlines = [
        CoworkingPhotoInline,
        TypeWorkingSpaceInline,
        WorkingSpaceInline,
    ]
