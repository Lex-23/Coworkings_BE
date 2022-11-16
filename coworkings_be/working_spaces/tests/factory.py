import decimal

import factory
from coworking.tests.factory import CoworkingFactory
from factory.django import DjangoModelFactory
from working_spaces.models import TypeWorkingSpace, WorkingSpace


class TypeWorkingSpaceFactory(DjangoModelFactory):
    class Meta:
        model = TypeWorkingSpace

    coworking = factory.SubFactory(CoworkingFactory)
    base_price = decimal.Decimal("10.50")


class WorkingSpaceFactory(DjangoModelFactory):
    class Meta:
        model = WorkingSpace

    coworking = factory.SubFactory(CoworkingFactory)
    type = factory.SubFactory(TypeWorkingSpaceFactory)
    local_number = factory.Sequence(lambda n: n)
