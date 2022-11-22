import datetime

import factory
from factory.django import DjangoModelFactory
from psycopg2.extras import DateTimeTZRange
from reservation.models import Reservation
from users.tests.factory import UserFactory
from working_spaces.tests.factory import WorkingSpaceFactory

START_DATETIME = datetime.datetime(2022, 11, 1, 10, 00, 00)


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    user = factory.SubFactory(UserFactory)
    working_space = factory.SubFactory(WorkingSpaceFactory)
    datetime_range = factory.Sequence(
        (
            lambda n: DateTimeTZRange(
                START_DATETIME + datetime.timedelta(days=n),
                START_DATETIME
                + datetime.timedelta(hours=8)
                + datetime.timedelta(days=n),
            )
        )
    )
