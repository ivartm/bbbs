from django.core.exceptions import ValidationError
from django.test import TestCase

from places.models import Place


class PlaceModelTest(TestCase):
    def test_place_activity_type_reqiured_field(self):
        place = Place(
            # activity_type= 1,
            title="123",
            address="1234",
            description="1235",
            age=10,
        )
        with self.assertRaises(
            ValidationError, msg="Поле activity_type должно быть обязательным"
        ):
            place.full_clean()

    def test_place_title_reqiured_field(self):
        place = Place(
            activity_type=1,
            # title="123",
            address="1234",
            description="1235",
            age=10,
        )
        with self.assertRaises(
            ValidationError, msg="Поле title должно быть обязательным"
        ):
            place.full_clean()

    def test_place_address_reqiured_field(self):
        place = Place(
            activity_type=1,
            title="123",
            # address="1234",
            description="1235",
            age=10,
        )
        with self.assertRaises(
            ValidationError, msg="Поле address должно быть обязательным"
        ):
            place.full_clean()

    def test_place_description_reqiured_field(self):
        place = Place(
            activity_type=1,
            title="123",
            address="1234",
            # description="1235",
            age=10,
        )
        with self.assertRaises(
            ValidationError, msg="Поле description должно быть обязательным"
        ):
            place.full_clean()

    def test_place_age_reqiured_field(self):
        place = Place(
            activity_type=1,
            title="123",
            address="1234",
            description="1235",
            # age=10
        )
        with self.assertRaises(
            ValidationError, msg="Поле age должно быть обязательным"
        ):
            place.full_clean()
