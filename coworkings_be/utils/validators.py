from rest_framework.exceptions import PermissionDenied
from users.models import UserRoles


def validate_request_to_coworking(user, user_role, owner):
    if user_role == UserRoles.OWNER and user != owner:
        raise PermissionDenied(
            {
                "detail": "You are not a owner of this coworking. You haven`t permissions for this operation."
            }
        )
    if user_role == UserRoles.GUEST:
        raise PermissionDenied()


def validate_request_to_reservation(user, reservation):
    if reservation.user != user and user.role != UserRoles.ADMINISTRATOR:
        raise PermissionDenied(
            {"detail": "You do not have access to this reservation."}
        )
