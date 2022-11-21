import datetime
import decimal

from django.db import connection, transaction
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from psycopg2.extras import DateTimeTZRange
from reservation.models import Reservation
from reservation.tests.factory import ReservationFactory
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from users.models import UserRoles
from users.serializers import CustomTokenObtainPairSerializer
from users.tests.factory import UserFactory
from working_spaces.tests.factory import WorkingSpaceFactory

from coworkings_be.settings import REST_FRAMEWORK as DRF


class ReservationListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.reservation_list = ReservationFactory.create_batch(5)
        self.url = reverse("list_reservation")
        self.maxDiff = None

    def test_get_list_reservation(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.client.force_authenticate(user=self.user, token=token)
        data = self.reservation_list
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(data), response.json()["count"])

        for expected_data, actual_data in zip(data, response.json()["results"]):
            self.assertEqual(expected_data.id, actual_data["id"])
            self.assertEqual(
                expected_data.working_space.id, actual_data["working_space"]
            )
            self.assertEqual(
                expected_data.datetime_range.lower.strftime(
                    format=DRF["DATETIME_FORMAT"]
                ),
                actual_data["start_time"],
            )
            self.assertEqual(
                expected_data.datetime_range.upper.strftime(
                    format=DRF["DATETIME_FORMAT"]
                ),
                actual_data["end_time"],
            )
            self.assertEqual(
                expected_data.total_price(), decimal.Decimal(actual_data["total_price"])
            )
            self.assertEqual(expected_data.paid, actual_data["paid"])

    def test_db_calls(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.client.force_authenticate(user=self.user, token=token)

        with CaptureQueriesContext(connection) as query_context:
            self.client.get(self.url)

        self.assertEqual(2, len(query_context))

        self.coworking_list = ReservationFactory.create_batch(10)
        with CaptureQueriesContext(connection) as query_context:
            self.client.get(self.url)
        self.assertEqual(2, len(query_context))

    def test_get_list_reservation_not_auth_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "Authentication credentials were not provided."},
            response.json(),
        )


class ReservationDetailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.reservation = ReservationFactory(
            user=self.user,
            datetime_range=DateTimeTZRange(
                datetime.datetime(2022, 12, 1, 10, 00, 00),
                datetime.datetime(2022, 12, 1, 18, 00, 00),
            ),
        )
        self.url = reverse("detail_reservation", kwargs={"pk": self.reservation.id})
        self.maxDiff = None

    def test_get_reservation_not_auth_user(self):
        response = self.client.get(self.url)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "Authentication credentials were not provided."}, response.json()
        )

    def test_delete_reservation_not_auth_user(self):
        response = self.client.delete(self.url)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "Authentication credentials were not provided."}, response.json()
        )

    def test_get_and_delete_reservation_by_another_user(self):
        user = UserFactory()
        token = CustomTokenObtainPairSerializer.get_token(user)
        self.client.force_authenticate(user=user, token=token)
        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)
        self.assertEqual(
            {"detail": "You do not have access to this reservation."}, response.json()
        )

        response1 = self.client.delete(self.url)

        self.assertEqual(403, response1.status_code)
        self.assertEqual(
            {"detail": "You do not have access to this reservation."}, response.json()
        )

    def test_get_and_delete_reservation(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.client.force_authenticate(user=self.user, token=token)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.reservation.id, response.json()["id"])
        self.assertEqual(
            self.reservation.working_space.id, response.json()["working_space"]
        )

        response1 = self.client.delete(self.url)

        self.assertEqual(204, response1.status_code)
        with self.assertRaises(Reservation.DoesNotExist):
            Reservation.objects.get(id=self.reservation.id)

    def test_get_and_delete_reservation_by_administrator(self):
        user = UserFactory(role=UserRoles.ADMINISTRATOR)
        token = CustomTokenObtainPairSerializer.get_token(user)
        self.client.force_authenticate(user=user, token=token)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.reservation.id, response.json()["id"])
        self.assertEqual(
            self.reservation.working_space.id, response.json()["working_space"]
        )

        response1 = self.client.delete(self.url)

        self.assertEqual(204, response1.status_code)
        with self.assertRaises(Reservation.DoesNotExist):
            Reservation.objects.get(id=self.reservation.id)


class ReservationCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.start_time = datetime.datetime(2022, 12, 2, 10, 00, 00)
        self.end_time = datetime.datetime(2022, 12, 2, 18, 00, 00)
        self.working_space = WorkingSpaceFactory()
        self.url = reverse("list_reservation")
        self.maxDiff = None

    def create_reservation(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.client.force_authenticate(user=self.user, token=token)
        data = {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "working_space": self.working_space.id,
        }
        return self.client.post(self.url, data=data)

    def test_create_reservation(self):
        response = self.create_reservation()
        self.assertEqual(201, response.status_code)

        expected_data = response.json()
        actual_data = Reservation.objects.get(id=expected_data["id"])

        self.assertEqual(
            actual_data.datetime_range.lower.strftime(format=DRF["DATETIME_FORMAT"]),
            expected_data["start_time"],
        )
        self.assertEqual(
            actual_data.datetime_range.upper.strftime(format=DRF["DATETIME_FORMAT"]),
            expected_data["end_time"],
        )
        self.assertEqual(actual_data.working_space.id, expected_data["working_space"])
        self.assertEqual(self.user.id, expected_data["user"])

    def test_create_reservation_overlaps_time(self):
        self.create_reservation()
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.client.force_authenticate(user=self.user, token=token)

        items = (
            {
                "case": "overlaps in start",
                "data": {
                    "start_time": self.start_time - datetime.timedelta(seconds=60),
                    "end_time": self.end_time - datetime.timedelta(seconds=60),
                    "working_space": self.working_space.id,
                },
            },
            {
                "case": "overlaps in end",
                "data": {
                    "start_time": self.start_time + datetime.timedelta(seconds=60),
                    "end_time": self.end_time + datetime.timedelta(seconds=60),
                    "working_space": self.working_space.id,
                },
            },
            {
                "case": "overlaps in middle",
                "data": {
                    "start_time": self.start_time + datetime.timedelta(seconds=60),
                    "end_time": self.end_time - datetime.timedelta(seconds=60),
                    "working_space": self.working_space.id,
                },
            },
            {
                "case": "overlaps at all",
                "data": {
                    "start_time": self.start_time - datetime.timedelta(seconds=60),
                    "end_time": self.end_time + datetime.timedelta(seconds=60),
                    "working_space": self.working_space.id,
                },
            },
        )

        for item in items:
            with self.subTest(item["case"]), transaction.atomic():
                response = self.client.post(self.url, data=item["data"])
                breakpoint()
                self.assertEqual(400, response.status_code)
                self.assertEqual(
                    {
                        "error_message": "This time overlaps another time for this working space"
                    },
                    response.json(),
                )
