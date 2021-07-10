from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from common.factories import CityFactory
from places.factories import PlaceFactory, PlacesTagFactory


class PlaceModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.city = CityFactory(name="Учтюпинск")
        cls.tag = PlacesTagFactory(name="test")
        cls.place = PlaceFactory(tags=[cls.tag])

    def test_place_activity_type_required_field(self):
        place = self.place
        place.activity_type = ""
        with self.assertRaises(
            ValidationError, msg="Поле activity_type должно быть обязательным"
        ):
            place.full_clean()

    def test_place_title_required_field(self):
        place = self.place
        place.title = ""
        with self.assertRaises(
            ValidationError, msg="Поле title должно быть обязательным"
        ):
            place.full_clean()

    def test_place_address_required_field(self):
        place = self.place
        place.address = ""
        with self.assertRaises(
            ValidationError, msg="Поле address должно быть обязательным"
        ):
            place.full_clean()

    def test_place_description_required_field(self):
        place = self.place
        place.description = ""
        with self.assertRaises(
            ValidationError, msg="Поле description должно быть обязательным"
        ):
            place.full_clean()

    def test_place_age_required_field(self):
        place = self.place
        place.age = ""
        with self.assertRaises(
            ValidationError, msg="Поле age должно быть обязательным"
        ):
            place.full_clean()

    def test_place_tag_required_field(self):
        place = self.place
        place.tags.clear()
        with self.assertRaises(
            ValidationError, msg="Поле tag должно быть обязательным"
        ):
            place.full_clean()

    def test_unique_place_for_city_constraint(self):
        city = CityFactory()
        address = "Абонентский ящик АЯ 23"
        title = "Место 1"

        PlaceFactory(city=city, address=address, title=title)

        with self.assertRaises(
            IntegrityError,
            msg=(
                "Убедитесь, что нельзя создать место с одним названием, "
                "адресом и городом."
            ),
        ):
            PlaceFactory(city=city, address=address, title=title)
