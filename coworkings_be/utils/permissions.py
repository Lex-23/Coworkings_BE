from rest_framework import permissions
from users.models import UserRoles


class IsOwnerOrAdministratorRoleOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or administrators to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.auth["user_role"] != UserRoles.GUEST
