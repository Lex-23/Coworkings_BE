from coworking.models import Coworking
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from utils.permissions import IsOwnerOrAdministratorRoleOrReadOnly
from utils.validators import validate_request_to_coworking
from working_spaces.models import TypeWorkingSpace, WorkingSpace
from working_spaces.serializers import (
    TypeWorkingSpaceSerializer,
    WorkingSpaceSerializer,
)


class WorkingSpaceListView(ListCreateAPIView):
    permission_classes = (IsOwnerOrAdministratorRoleOrReadOnly,)
    queryset = WorkingSpace.objects.all()
    serializer_class = WorkingSpaceSerializer

    def create(self, request, *args, **kwargs):
        coworking = get_object_or_404(
            queryset=Coworking.objects.all(), pk=request.data["coworking"]
        )
        validate_request_to_coworking(
            request.user, request.auth["user_role"], coworking.owner
        )
        return super().create(request, *args, **kwargs)


class WorkingSpaceDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrAdministratorRoleOrReadOnly,)
    queryset = WorkingSpace.objects.all()
    serializer_class = WorkingSpaceSerializer

    def validate_request(self, request):
        coworking = Coworking.objects.get(id=self.get(request).data["coworking"])
        validate_request_to_coworking(
            request.user, request.auth["user_role"], coworking.owner
        )

    def partial_update(self, request, *args, **kwargs):
        self.validate_request(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.validate_request(request)
        return super().destroy(request, *args, **kwargs)


class TypeWorkingSpaceListView(ListCreateAPIView):
    permission_classes = (IsOwnerOrAdministratorRoleOrReadOnly,)
    queryset = TypeWorkingSpace.objects.all()
    serializer_class = TypeWorkingSpaceSerializer

    def create(self, request, *args, **kwargs):
        coworking = get_object_or_404(
            queryset=Coworking.objects.all(), pk=request.data["coworking"]
        )
        validate_request_to_coworking(
            request.user, request.auth["user_role"], coworking.owner
        )
        return super().create(request, *args, **kwargs)


class TypeWorkingSpaceDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrAdministratorRoleOrReadOnly,)
    queryset = TypeWorkingSpace.objects.all()
    serializer_class = TypeWorkingSpaceSerializer

    def validate_request(self, request):
        coworking = Coworking.objects.get(id=self.get(request).data["coworking"])
        validate_request_to_coworking(
            request.user, request.auth["user_role"], coworking.owner
        )

    def partial_update(self, request, *args, **kwargs):
        self.validate_request(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.validate_request(request)
        return super().destroy(request, *args, **kwargs)
