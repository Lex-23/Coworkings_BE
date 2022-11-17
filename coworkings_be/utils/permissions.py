from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from users.models import UserRoles


class IsOwnerOrAdministratorRoleOrReadOnly(permissions.BasePermission):
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
