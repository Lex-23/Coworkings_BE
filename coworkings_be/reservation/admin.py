from django.contrib import admin
from reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    fields = ("user", "working_space", "datetime_range", "paid")
    list_display = (
        "id",
        "user",
        "coworking",
        "working_space",
        "start_time",
        "end_time",
        "duration",
        "total_price",
        "paid",
    )
    search_fields = (
        "user__email",
        "working_space__coworking__title",
        "working_space__individual_number",
        "start_time",
        "end_time",
    )
    list_editable = ("paid",)
    ordering = ("working_space__coworking", "datetime_range")
    list_per_page = 30

    def has_add_permission(self, request, obj=None):
        return False


class ReservationInline(admin.TabularInline):
    model = Reservation
    fields = ("user", "working_space", "datetime_range", "paid")
    extra = 1
