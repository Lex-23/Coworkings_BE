import factory
from django.contrib.auth import get_user_model
from factory import fuzzy
from users.models import UserRoles

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user_email{n}@gmail.com")
    password = fuzzy.FuzzyText(length=8)
    role = UserRoles.OWNER
