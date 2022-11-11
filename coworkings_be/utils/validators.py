from rest_framework.exceptions import PermissionDenied
from users.models import UserRoles


def validate_request_to_coworking(request, owner):
    if request.auth["user_role"] == UserRoles.OWNER and request.user != owner:
        raise PermissionDenied(
            {
                "detail": "You are not a owner of this coworking. You haven`t permissions for this operation."
            }
        )
    if request.auth["user_role"] == UserRoles.GUEST:
        raise PermissionDenied()
