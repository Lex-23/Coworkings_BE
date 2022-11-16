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


class BaseWorkingSpaceListView(ListCreateAPIView):
    permission_classes = (IsOwnerOrAdministratorRoleOrReadOnly,)

    def post(self, request, *args, **kwargs):
        coworking = get_object_or_404(
            queryset=Coworking.objects.all(), pk=request.data["coworking"]
        )
        validate_request_to_coworking(
            request.user, request.auth["user_role"], coworking.owner
        )
        return self.create(request, *args, **kwargs)


class BaseWorkingSpaceDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrAdministratorRoleOrReadOnly,)

    def validate_request(self, request):
        coworking = Coworking.objects.get(id=self.get(request).data["coworking"])
        validate_request_to_coworking(
            request.user, request.auth["user_role"], coworking.owner
        )

    def patch(self, request, *args, **kwargs):
        self.validate_request(request)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.validate_request(request)
        return self.destroy(request, *args, **kwargs)


class WorkingSpaceListView(BaseWorkingSpaceListView):
    queryset = WorkingSpace.objects.all()
    serializer_class = WorkingSpaceSerializer


class WorkingSpaceDetailView(BaseWorkingSpaceDetailView):
    queryset = WorkingSpace.objects.all()
    serializer_class = WorkingSpaceSerializer


class TypeWorkingSpaceListView(BaseWorkingSpaceListView):
    queryset = TypeWorkingSpace.objects.all()
    serializer_class = TypeWorkingSpaceSerializer


class TypeWorkingSpaceDetailView(BaseWorkingSpaceDetailView):
    queryset = TypeWorkingSpace.objects.all()
    serializer_class = TypeWorkingSpaceSerializer
