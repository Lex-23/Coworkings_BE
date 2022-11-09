from coworking.models import Coworking, CoworkingPhoto
from rest_framework import serializers
from users.models import CustomUser


class CoworkingPhotoSerializer(serializers.ModelSerializer):
    queryset = Coworking.objects.all()
    coworking = serializers.PrimaryKeyRelatedField(queryset=queryset)
    hashtags = serializers.StringRelatedField(many=True)

    class Meta:
        model = CoworkingPhoto
        fields = "__all__"


class CoworkingSerializer(serializers.ModelSerializer):
    owners_queryset = CustomUser.objects.all()
    owner = serializers.PrimaryKeyRelatedField(queryset=owners_queryset, required=False)
    photos = CoworkingPhotoSerializer(many=True, required=False)

    class Meta:
        model = Coworking
        fields = "__all__"
        extra_fields = ["photos"]
