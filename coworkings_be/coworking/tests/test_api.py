from coworking.models import Coworking
from coworking.tests.factory import CoworkingFactory
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from users.models import UserRoles
from users.serializers import CustomTokenObtainPairSerializer
from users.tests.factory import TestUsersMixin, UserFactory

User = get_user_model()


class CoworkingListTestCase(TestCase, TestUsersMixin):
    def setUp(self):
        self.client = APIClient()
        self.coworking_list = CoworkingFactory.create_batch(
            10, owner=UserFactory(role=UserRoles.OWNER)
        )
        self.url = reverse("coworking-list")
        self.maxDiff = None

    def test_get_list_coworking(self):
        response = self.client.get(self.url)
        data = self.coworking_list
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(data), response.json()["count"])
        for n in range(len(data)):
            self.assertEqual(data[n].id, response.json()["results"][n]["id"])
            self.assertEqual(data[n].owner.id, response.json()["results"][n]["owner"])
            self.assertEqual(
                list(data[n].photos), response.json()["results"][n]["photos"]
            )
            self.assertEqual(data[n].title, response.json()["results"][n]["title"])
            self.assertEqual(
                data[n].description, response.json()["results"][n]["description"]
            )
            self.assertEqual(data[n].city, response.json()["results"][n]["city"])
            self.assertEqual(data[n].address, response.json()["results"][n]["address"])
            self.assertEqual(
                data[n].opening_time, response.json()["results"][n]["opening_time"]
            )
            self.assertEqual(
                data[n].closing_time, response.json()["results"][n]["closing_time"]
            )
            self.assertEqual(data[n].avatar, response.json()["results"][n]["avatar"])
            self.assertEqual(data[n].status, response.json()["results"][n]["status"])

    def test_db_calls(self):
        with CaptureQueriesContext(connection) as query_context:
            self.client.get(self.url)
        self.assertEqual(3, len(query_context))

    def test_create_coworking_not_auth_user(self):
        data = {
            "title": "New coworking",
            "owner": UserFactory(role=UserRoles.OWNER),
            "city": "Minsk",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "You must be authenticated in system for this operation"},
            response.json(),
        )

    def test_create_coworking_auth_user_owner(self):

        user_owner = self.test_users["owner"]

        data = {"title": "New coworking", "city": "Minsk"}
        token = CustomTokenObtainPairSerializer.get_token(user_owner)
        self.client.force_authenticate(user=user_owner, token=token)
        response = self.client.post(self.url, data=data)
        new_coworking = Coworking.objects.get(id=response.json()["id"])

        self.assertEqual(201, response.status_code)
        self.assertEqual(data["title"], response.json()["title"])
        self.assertEqual(data["city"], response.json()["city"])
        self.assertEqual(new_coworking.owner.id, user_owner.id)

    def test_create_coworking_auth_user_administrator(self):

        user_administrator = self.test_users["administrator"]

        data = {
            "title": "New coworking1",
            "city": "Minsk",
            "owner": UserFactory(role=UserRoles.OWNER).id,
        }
        token = CustomTokenObtainPairSerializer.get_token(user_administrator)
        self.client.force_authenticate(user=user_administrator, token=token)
        response = self.client.post(self.url, data=data)
        new_coworking = Coworking.objects.get(id=response.json()["id"])

        self.assertEqual(201, response.status_code)
        self.assertEqual(data["title"], response.json()["title"])
        self.assertEqual(data["city"], response.json()["city"])
        self.assertEqual(new_coworking.owner.id, data["owner"])

    def test_create_coworking_auth_user_guest(self):

        user_guest = self.test_users["guest"]

        data = {
            "title": "New coworking1",
            "city": "Minsk",
        }
        token = CustomTokenObtainPairSerializer.get_token(user_guest)
        self.client.force_authenticate(user=user_guest, token=token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response.json(),
        )


class CoworkingItemTestCase(TestCase, TestUsersMixin):
    def setUp(self):
        self.client = APIClient()
        self.coworking_owner = User.objects.create_user(
            email="owner@test.com", password="some_pass", role=UserRoles.OWNER
        )
        self.coworking = CoworkingFactory(owner=self.coworking_owner)
        self.url = reverse("coworking-item", kwargs={"pk": self.coworking.id})
        self.maxDiff = None

    def test_get_coworking_not_auth_user(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.coworking.id, response.json()["id"])
        self.assertEqual(self.coworking.title, response.json()["title"])

    def test_patch_coworking_not_auth_user(self):
        data = {"description": "description"}
        response = self.client.patch(self.url, data)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "Authentication credentials were not provided."}, response.json()
        )

    def test_delete_coworking_not_auth_user(self):
        response = self.client.delete(self.url)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "Authentication credentials were not provided."}, response.json()
        )

    def test_delete_and_patch_coworking_guest_user(self):
        user_guest = self.test_users["guest"]
        data = {"description": "description"}
        token = CustomTokenObtainPairSerializer.get_token(user_guest)
        self.client.force_authenticate(user=user_guest, token=token)

        response = self.client.patch(self.url, data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response.json(),
        )

        response1 = self.client.delete(self.url)
        self.assertEqual(403, response1.status_code)
        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response1.json(),
        )

    def test_delete_and_patch_coworking_another_owner_user(self):
        user_owner = self.test_users["owner"]
        data = {"description": "description"}
        token = CustomTokenObtainPairSerializer.get_token(user_owner)
        self.client.force_authenticate(user=user_owner, token=token)

        response = self.client.patch(self.url, data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            {
                "detail": "You are not a owner of this coworking. You haven`t permissions for this operation."
            },
            response.json(),
        )

        response1 = self.client.delete(self.url)
        self.assertEqual(403, response1.status_code)
        self.assertEqual(
            {
                "detail": "You are not a owner of this coworking. You haven`t permissions for this operation."
            },
            response1.json(),
        )

    def test_delete_and_patch_coworking_self_owner_user(self):
        data = {"description": "description"}
        token = CustomTokenObtainPairSerializer.get_token(self.coworking_owner)
        self.client.force_authenticate(user=self.coworking_owner, token=token)

        response = self.client.patch(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.coworking.id, response.json()["id"])
        self.assertEqual(self.coworking.id, response.json()["id"])
        self.assertEqual(
            Coworking.objects.get(id=self.coworking.id).description, data["description"]
        )

        response1 = self.client.delete(self.url)
        self.assertEqual(204, response1.status_code)
        with self.assertRaises(Coworking.DoesNotExist):
            Coworking.objects.get(id=self.coworking.id)

    def test_delete_and_patch_coworking_administrator_user(self):
        user_administrator = self.test_users["administrator"]
        data = {"description": "description"}
        token = CustomTokenObtainPairSerializer.get_token(user_administrator)
        self.client.force_authenticate(user=user_administrator, token=token)

        response = self.client.patch(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.coworking.id, response.json()["id"])
        self.assertEqual(self.coworking.id, response.json()["id"])
        self.assertEqual(
            Coworking.objects.get(id=self.coworking.id).description, data["description"]
        )

        response1 = self.client.delete(self.url)
        self.assertEqual(204, response1.status_code)
        with self.assertRaises(Coworking.DoesNotExist):
            Coworking.objects.get(id=self.coworking.id)
