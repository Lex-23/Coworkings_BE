from coworking.models import Coworking
from coworking.serializers import CoworkingRelatedSerializer
from rest_framework import serializers
from working_spaces.models import TypeWorkingSpace, WorkingSpace


class TypeWorkingSpaceSerializer(CoworkingRelatedSerializer):
    coworking = serializers.PrimaryKeyRelatedField(queryset=Coworking.objects.all())
    type = serializers.IntegerField()

    class Meta:
        model = TypeWorkingSpace
        fields = "__all__"


class WorkingSpaceSerializer(CoworkingRelatedSerializer):
    coworking = serializers.PrimaryKeyRelatedField(queryset=Coworking.objects.all())
    type = serializers.PrimaryKeyRelatedField(queryset=TypeWorkingSpace.objects.all())

    class Meta:
        model = WorkingSpace
        fields = "__all__"
