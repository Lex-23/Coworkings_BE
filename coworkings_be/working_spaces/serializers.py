from coworking.models import Coworking
from coworking.serializers import CoworkingRelatedSerializer
from rest_framework import serializers
from working_spaces.models import TypeWorkingSpace, WorkingSpace


class TypeWorkingSpaceSerializer(CoworkingRelatedSerializer):
    queryset = Coworking.objects.all()
    coworking = serializers.PrimaryKeyRelatedField(queryset=queryset, required=False)
    type = serializers.IntegerField(required=False)

    class Meta:
        model = TypeWorkingSpace
        fields = "__all__"


class WorkingSpaceSerializer(CoworkingRelatedSerializer):
    coworking_queryset = Coworking.objects.all()
    coworking = serializers.PrimaryKeyRelatedField(
        queryset=coworking_queryset, required=False
    )
    type_queryset = TypeWorkingSpace.objects.all()
    type = serializers.PrimaryKeyRelatedField(queryset=type_queryset, required=False)

    class Meta:
        model = WorkingSpace
        fields = "__all__"