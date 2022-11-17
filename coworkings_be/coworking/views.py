from coworking.models import Coworking
from coworking.serializers import CoworkingSerializer
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.permissions import IsOwnerOrAdministratorRoleOrReadOnly
from utils.validators import validate_request_to_coworking


class CoworkingView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        return get_object_or_404(queryset=Coworking.objects.all(), pk=pk)

    def get(self, request, pk, format=None):
        coworking = self.get_object(pk)
        serializer = CoworkingSerializer(coworking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        coworking = self.get_object(pk)
        validate_request_to_coworking(
            request.user, request.auth["user_role"], coworking.owner
        )
        serializer = CoworkingSerializer(coworking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        coworking = self.get_object(pk)
        validate_request_to_coworking(
            request.user, request.auth["user_role"], coworking.owner
        )
        coworking.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CoworkingListView(APIView, LimitOffsetPagination):
    permission_classes = (IsOwnerOrAdministratorRoleOrReadOnly,)

    def get(self, request, format=None):
        coworkings = (
            Coworking.objects.select_related("owner")
            .prefetch_related("coworking_photo")
            .all()
        )
        results = self.paginate_queryset(coworkings, request, view=self)
        serializer = CoworkingSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = CoworkingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        owner = serializer.validated_data.pop("owner", request.user)
        new_coworking = Coworking.objects.create(
            owner=owner,
            **serializer.validated_data,
        )
        serializer = CoworkingSerializer(new_coworking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
