from rest_framework.exceptions import ValidationError


def validate_is_owner(request, owner):
    if request.user != owner:
        raise ValidationError(
            [
                "You are not a owner of this coworking. You haven`t permissions for this operation."
            ]
        )
