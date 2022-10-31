import decimal

from django.core.validators import MinValueValidator
from django.db import models


class PriceField(models.DecimalField):
    """default field for price"""

    MAX_DIGITS = 8
    DECIMAL_PLACES = 2
    VALIDATORS = [MinValueValidator(decimal.Decimal("0.01"))]

    def __init__(self, **kwargs):
        kwargs.setdefault("max_digits", self.MAX_DIGITS)
        kwargs.setdefault("decimal_places", self.DECIMAL_PLACES)
        kwargs.setdefault("validators", self.VALIDATORS)
        super().__init__(**kwargs)
