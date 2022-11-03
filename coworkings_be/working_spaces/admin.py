from django.contrib import admin
from reservation.admin import ReservationInline
from working_spaces.models import TypeWorkingSpace, WorkingSpace


class TypeWorkingSpaceInline(admin.TabularInline):
    model = TypeWorkingSpace
    fields = ("coworking", "type", "label", "base_price")
    extra = 0


class WorkingSpaceInline(admin.TabularInline):
    model = WorkingSpace
    fields = ("type", "local_number")
    extra = 1


@admin.register(TypeWorkingSpace)
class TypeWorkingSpaceAdmin(admin.ModelAdmin):
    fields = ("coworking", "type", "label", "base_price")
    list_display = ("id", "coworking", "type", "label", "base_price")
    search_fields = ("coworking__title",)
    list_filter = ("type",)
    ordering = ("coworking", "type")
    readonly_fields = ["coworking"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(WorkingSpace)
class WorkingSpaceAdmin(admin.ModelAdmin):
    fields = ("type", "coworking", "local_number")
    list_display = (
        "id",
        "coworking",
        "type",
        "local_number",
        "base_price",
        "individual_number",
    )
    search_fields = ("coworking__title",)
    list_filter = ("type",)
    ordering = ("coworking", "type", "local_number")
    readonly_fields = ["coworking"]
    inlines = [ReservationInline]

    def has_add_permission(self, request, obj=None):
        return False
