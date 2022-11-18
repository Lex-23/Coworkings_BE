from django.db import IntegrityError
from psycopg2.extras import DateTimeTZRange
from reservation.models import Reservation
from reservation.serializers import ReservationSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from utils.validators import validate_request_to_reservation


class ReservationListView(ListCreateAPIView):
    queryset = Reservation.objects.select_related(
        "working_space", "working_space__type"
    ).all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        datetime_range = DateTimeTZRange(data["start_time"], data["end_time"])

        try:
            new_object = Reservation.objects.create(
                datetime_range=datetime_range,
                user=data["user"],
                working_space=data["working_space"],
            )
        except IntegrityError:
            return Response(
                {
                    "error_message": "This time overlaps another time for this working space"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"id": new_object.id, **serializer.data}, status=status.HTTP_201_CREATED
        )


class ReservationDetailView(RetrieveDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def retrieve(self, request, *args, **kwargs):
        reservation = self.get_object()
        validate_request_to_reservation(request.user, reservation)
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        validate_request_to_reservation(request.user, reservation)
        return super().destroy(request, *args, **kwargs)
