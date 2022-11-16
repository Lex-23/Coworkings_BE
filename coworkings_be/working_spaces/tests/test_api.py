from coworking.tests.factory import CoworkingFactory
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from users.models import UserRoles
from users.serializers import CustomTokenObtainPairSerializer
from users.tests.factory import UserFactory
from working_spaces.models import WorkingSpace
from working_spaces.tests.factory import TypeWorkingSpaceFactory, WorkingSpaceFactory

User = get_user_model()


class WorkingSpaceListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.working_space_list = WorkingSpaceFactory.create_batch(10)
        self.url = reverse("list_working_space")
        self.maxDiff = None

    def test_get_list_working_spaces(self):
        response = self.client.get(self.url)
        data = self.working_space_list
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(data), response.json()["count"])
        for expected_data, actual_data in zip(data, response.json()["results"]):
            self.assertEqual(expected_data.coworking.id, actual_data["coworking"])
            self.assertEqual(expected_data.id, actual_data["id"])
            self.assertEqual(expected_data.type.id, actual_data["type"])
            self.assertEqual(expected_data.local_number, actual_data["local_number"])
            self.assertEqual(
                str(expected_data.individual_number), actual_data["individual_number"]
            )

    def test_db_calls(self):
        with CaptureQueriesContext(connection) as query_context:
            self.client.get(self.url)
        self.assertEqual(2, len(query_context))

        self.working_space_list = WorkingSpaceFactory.create_batch(10)
        with CaptureQueriesContext(connection) as query_context:
            self.client.get(self.url)
        self.assertEqual(2, len(query_context))

    def test_create_working_space_not_auth_user(self):
        data = {
            "type": TypeWorkingSpaceFactory(),
            "local_number": 13,
            "coworking": CoworkingFactory(),
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "You must be authenticated in system for this operation"},
            response.json(),
        )

    def test_create_coworking_space_auth_user_owner(self):
        # user is owner for this coworking

        user_owner = UserFactory(role=UserRoles.OWNER)
        coworking = CoworkingFactory(owner=user_owner)

        data = {
            "type": TypeWorkingSpaceFactory().id,
            "local_number": 13,
            "coworking": coworking.id,
        }
        token = CustomTokenObtainPairSerializer.get_token(user_owner)
        self.client.force_authenticate(user=user_owner, token=token)
        response = self.client.post(self.url, data=data)
        new_working_space = WorkingSpace.objects.get(id=response.json()["id"])

        self.assertEqual(201, response.status_code)
        self.assertEqual(new_working_space.type.id, response.json()["type"])
        self.assertEqual(
            new_working_space.local_number, response.json()["local_number"]
        )
        self.assertEqual(new_working_space.coworking.id, response.json()["coworking"])

    def test_create_coworking_space_auth_user_owner_not(self):
        # user is not owner for this coworking

        user_owner = UserFactory(role=UserRoles.OWNER)
        coworking = CoworkingFactory()

        data = {
            "type": TypeWorkingSpaceFactory().id,
            "local_number": 13,
            "coworking": coworking.id,
        }
        token = CustomTokenObtainPairSerializer.get_token(user_owner)
        self.client.force_authenticate(user=user_owner, token=token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            {
                "detail": "You are not a owner of this coworking. You haven`t permissions for this operation."
            },
            response.json(),
        )

    #
    def test_create_coworking_space_auth_user_administrator(self):

        user_administrator = UserFactory(role=UserRoles.ADMINISTRATOR)
        coworking = CoworkingFactory()

        data = {
            "type": TypeWorkingSpaceFactory().id,
            "local_number": 13,
            "coworking": coworking.id,
        }
        token = CustomTokenObtainPairSerializer.get_token(user_administrator)
        self.client.force_authenticate(user=user_administrator, token=token)
        response = self.client.post(self.url, data=data)
        new_working_space = WorkingSpace.objects.get(id=response.json()["id"])

        self.assertEqual(201, response.status_code)
        self.assertEqual(new_working_space.type.id, response.json()["type"])
        self.assertEqual(
            new_working_space.local_number, response.json()["local_number"]
        )
        self.assertEqual(new_working_space.coworking.id, response.json()["coworking"])

    def test_create_coworking_space_auth_user_guest(self):

        user_guest = UserFactory(role=UserRoles.GUEST)

        coworking = CoworkingFactory()

        data = {
            "type": TypeWorkingSpaceFactory().id,
            "local_number": 13,
            "coworking": coworking.id,
        }
        token = CustomTokenObtainPairSerializer.get_token(user_guest)
        self.client.force_authenticate(user=user_guest, token=token)
        response = self.client.post(self.url, data=data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            {"detail": "You do not have permission to perform this action."},
            response.json(),
        )


class WorkingSpaceItemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.coworking_owner = User.objects.create_user(
            email="owner@test.com", password="some_pass", role=UserRoles.OWNER
        )
        self.coworking = CoworkingFactory(owner=self.coworking_owner)
        self.working_space = WorkingSpaceFactory(coworking=self.coworking)
        self.url = reverse("detail_working_space", kwargs={"pk": self.working_space.id})
        self.maxDiff = None

    def test_get_working_space_not_auth_user(self):
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.working_space.id, response.json()["id"])

    def test_patch_working_space_not_auth_user(self):
        data = {"local_number": self.working_space.local_number + 10}
        response = self.client.patch(self.url, data)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "You must be authenticated in system for this operation"},
            response.json(),
        )

    def test_delete_working_space_not_auth_user(self):
        response = self.client.delete(self.url)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "You must be authenticated in system for this operation"},
            response.json(),
        )

    def test_delete_and_patch_working_space_guest_user(self):
        user_guest = UserFactory(role=UserRoles.GUEST)
        data = {"local_number": self.working_space.local_number + 10}
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

    def test_delete_and_patch_working_space_another_owner_user(self):
        user_owner = UserFactory(role=UserRoles.OWNER)
        data = {"local_number": self.working_space.local_number + 10}
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

    def test_delete_and_patch_working_space_self_owner_user(self):
        data = {"local_number": self.working_space.local_number + 10}
        token = CustomTokenObtainPairSerializer.get_token(self.coworking_owner)
        self.client.force_authenticate(user=self.coworking_owner, token=token)
        response = self.client.patch(self.url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.working_space.id, response.json()["id"])
        self.assertEqual(
            WorkingSpace.objects.get(id=self.working_space.id).local_number,
            data["local_number"],
        )

        response1 = self.client.delete(self.url)

        self.assertEqual(204, response1.status_code)
        with self.assertRaises(WorkingSpace.DoesNotExist):
            WorkingSpace.objects.get(id=self.working_space.id)

    def test_delete_and_patch_coworking_administrator_user(self):
        user_administrator = UserFactory(role=UserRoles.ADMINISTRATOR)
        data = {"local_number": self.working_space.local_number + 10}
        token = CustomTokenObtainPairSerializer.get_token(user_administrator)
        self.client.force_authenticate(user=user_administrator, token=token)
        response = self.client.patch(self.url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.working_space.id, response.json()["id"])
        self.assertEqual(
            WorkingSpace.objects.get(id=self.working_space.id).local_number,
            data["local_number"],
        )

        response1 = self.client.delete(self.url)

        self.assertEqual(204, response1.status_code)
        with self.assertRaises(WorkingSpace.DoesNotExist):
            WorkingSpace.objects.get(id=self.working_space.id)


class TypeWorkingSpaceListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.type_working_space_list = TypeWorkingSpaceFactory.create_batch(10)
        self.url = reverse("list_type_working_space")
        self.maxDiff = None

    def test_get_list_working_spaces(self):
        response = self.client.get(self.url)
        data = self.type_working_space_list
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(data), response.json()["count"])

        for expected_data, actual_data in zip(data, response.json()["results"]):
            self.assertEqual(expected_data.id, actual_data["id"])
            self.assertEqual(expected_data.coworking.id, actual_data["coworking"])
            self.assertEqual(expected_data.type, actual_data["type"])
            self.assertEqual(expected_data.label, actual_data["label"])
            self.assertEqual(str(expected_data.base_price), actual_data["base_price"])

    def test_db_calls(self):
        with CaptureQueriesContext(connection) as query_context:
            self.client.get(self.url)
        self.assertEqual(2, len(query_context))

        self.type_working_space_list = TypeWorkingSpaceFactory.create_batch(100)
        with CaptureQueriesContext(connection) as query_context:
            self.client.get(self.url)
        self.assertEqual(2, len(query_context))


# other test cases same as for TypeWorkingSpace same as for WorkingSpace. We do not need them now.
