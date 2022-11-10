from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from users.models import UserRoles


class IsOwnerOrAdministratorRoleOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or administrators to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.auth is None:
            raise NotAuthenticated(
                "You must be authenticated in system for this operation"
            )
        elif request.auth["user_role"] == UserRoles.GUEST:
            raise PermissionDenied()
        else:
            return True
