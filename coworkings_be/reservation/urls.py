from django.urls import path
from reservation.views import ReservationDetailView, ReservationListView

urlpatterns = [
    path("reservation/", ReservationListView.as_view(), name="list_reservation"),
    path(
        "reservation/<int:pk>/",
        ReservationDetailView.as_view(),
        name="detail_reservation",
    ),
]
