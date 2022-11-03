from django.core.exceptions import ValidationError


def validate_hashtag(value: str):
    if value[0] != "#":
        raise ValidationError("hashtag must be start from '#' symbol")
