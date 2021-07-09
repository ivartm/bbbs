from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from afisha.factories import EventFactory
from common.factories import CityFactory


class EventModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory()
        cls.tomorrow = timezone.now() + timedelta(days=1)
        cls.future = timezone.now() + timedelta(days=60)
        cls.past = timezone.now() - timedelta(days=10)

    def test_event_endat_cant_be_less_startat(self):
        event = EventFactory(
            start_at=EventModelTest.future,
            end_at=EventModelTest.tomorrow,
        )

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=(
                "Проверьте дату окончания мероприятия: "
                "не может быть меньше даты начала"
            ),
        ):
            event.full_clean()

    def test_event_startat_cant_be_less_today(self):
        event = EventFactory(
            start_at=EventModelTest.past,
        )

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=(
                "Проверьте дату начала мероприятия: "
                "не может быть меньше текущей"
            ),
        ):
            event.full_clean()

    def test_event_seats_must_more_than_one(self):
        event = EventFactory(
            seats=0,
        )

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=("Число мест должно быть больше нуля"),
        ):
            event.full_clean()
