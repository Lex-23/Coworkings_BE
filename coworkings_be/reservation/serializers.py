from reservation.models import Reservation
from rest_framework import serializers
from users.models import CustomUser
from working_spaces.models import WorkingSpace


class CreateReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    working_space = serializers.PrimaryKeyRelatedField(
        queryset=WorkingSpace.objects.all()
    )
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    class Meta:
        model = Reservation
        exclude = ("datetime_range",)
        extra_fields = ["start_time", "end_time"]

    def validate(self, attrs):
        if attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError(
                {"reservation time": "end time must be late than start time."}
            )
        return attrs


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    working_space = serializers.PrimaryKeyRelatedField(
        queryset=WorkingSpace.objects.all()
    )  # end_time = serializers.DateTimeField(required=False)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "user",
            "working_space",
            "start_time",
            "end_time",
            "total_price",
            "paid",
        )
