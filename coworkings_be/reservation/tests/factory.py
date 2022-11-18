import datetime

import factory
from factory.django import DjangoModelFactory
from psycopg2.extras import DateTimeTZRange
from reservation.models import Reservation
from users.tests.factory import UserFactory
from working_spaces.tests.factory import WorkingSpaceFactory

test_dates = [
    (
        datetime.datetime(2022, 11, n, 10, 00, 00),
        datetime.datetime(2022, 11, n, 18, 00, 00),
    )
    for n in range(1, 31)
]


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    user = factory.SubFactory(UserFactory)
    working_space = factory.SubFactory(WorkingSpaceFactory)
    datetime_range = factory.Sequence(
        (lambda n: DateTimeTZRange(test_dates[n][0], test_dates[n][1]))
    )
