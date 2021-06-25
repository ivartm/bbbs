from django.core.exceptions import ValidationError
from django.test import TestCase

from places.models import Place, PlaceTag


class PlaceModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        tag = PlaceTag.objects.create(name="test", slug="test")
        place = Place.objects.create(
            activity_type=1,
            title="123",
            address="1234",
            description="1235",
            age=10,
        )
        place.tags.add(tag)
        cls.place = place

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
