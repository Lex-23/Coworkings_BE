from django.contrib import admin
from reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    fields = ("user", "working_space", "start_time", "end_time", "total_price")
    list_display = (
        "id",
        "user",
        "coworking",
        "working_space",
        "start_time",
        "end_time",
        "total_price",
    )
    search_fields = (
        "user__email",
        "working_space__coworking__title",
        "working_space__individual_number",
    )
    list_editable = ("start_time", "end_time", "total_price")
    ordering = ("start_time", "end_time")
    list_per_page = 30

    def has_add_permission(self, request, obj=None):
        return False


class ReservationInline(admin.TabularInline):
    model = Reservation
    fields = ("user", "working_space", "start_time", "end_time", "total_price")
    extra = 1
