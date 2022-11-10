import factory
from django.contrib.auth import get_user_model
from users.models import UserRoles

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    role = UserRoles.OWNER


class TestUsersMixin:
    """
    This class create three users with 3 different roles for tests
    """

    @property
    def test_users(self):
        user_owner = User.objects.create_user(
            email="test_owner@test.com", password="some_pass", role=UserRoles.OWNER
        )
        user_administrator = User.objects.create_user(
            email="test_administrator@test.com",
            password="some_pass",
            role=UserRoles.ADMINISTRATOR,
        )
        user_guest = User.objects.create_user(
            email="test_guest@test.com", password="some_pass2"
        )
        return {
            "guest": user_guest,
            "owner": user_owner,
            "administrator": user_administrator,
        }
