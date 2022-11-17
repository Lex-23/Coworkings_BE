from django.db import IntegrityError
from psycopg2.extras import DateTimeTZRange
from reservation.models import Reservation
from reservation.serializers import CreateReservationSerializer, ReservationSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from utils.validators import validate_request_to_reservation


class ReservationListView(ListCreateAPIView):
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReservationSerializer
        elif self.request.method == "POST":
            return CreateReservationSerializer

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
        serializer = ReservationSerializer(new_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
