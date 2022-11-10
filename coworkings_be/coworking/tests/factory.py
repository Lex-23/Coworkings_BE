import factory
from coworking.models import Coworking
from factory.django import DjangoModelFactory
from users.tests.factory import UserFactory


class CoworkingFactory(DjangoModelFactory):
    class Meta:
        model = Coworking

    title = factory.Sequence(lambda n: f"Coworking#{n:03}")
    owner = factory.SubFactory(UserFactory)
    city = "Tbilisi"
