from tempfile import mkdtemp as tempfile_mkdtemp

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, override_settings

from bbbs.common.factories import CityFactory
from bbbs.places.factories import PlaceFactory, PlacesTagFactory
from bbbs.places.models import Place
from bbbs.users.factories import UserFactory
from bbbs.users.models import Profile

PLACES = reverse("places")
PLACES_TAGS = reverse("places-tags")

TEMP_DIR = tempfile_mkdtemp()


def get_temporary_image():
    small_gif = (
        b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
        b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
        b"\x02\x4c\x01\x00\x3b"
    )
    uploaded = SimpleUploadedFile(
        "small.gif",
        small_gif,
        content_type="image/gif",
    )
    return uploaded


@override_settings(MEDIA_ROOT=TEMP_DIR)
class ViewPlacesTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory(name="Тула")
        cls.mentor = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=cls.city,
        )
        PlaceFactory.create_batch(10, city=cls.city)
        cls.unauthorized_client = APIClient()

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_unauthorized_user_required_city_query_param(self):
        """
        PLACES and PLACES_TAGS should return error for unath users on GET
        without 'city' query param.
        """
        client = ViewPlacesTests.unauthorized_client

        for path in [PLACES, PLACES_TAGS]:
            with self.subTest(path):
                response = client.get(path)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                    msg=(
                        f"Проверьте что неавторизованный пользователь при GET "
                        f"запросе '{path}' получает ошибку."
                    ),
                )

    def test_unauthorized_user_with_city_query_param_receive_200(self):
        """
        PLACES and PLACES_TAGS should return HTTP_200_OK for unath users on GET
        with 'city' query param.
        """
        client = ViewPlacesTests.unauthorized_client
        query_param = {"city": ViewPlacesTests.city.id}

        for path in [PLACES, PLACES_TAGS]:
            with self.subTest(path):
                response = client.get(path, query_param)

                self.assertEqual(
                    response.status_code,
                    status.HTTP_200_OK,
                    msg=(
                        f"Проверьте что GET запросы к '{path}' с query "
                        f"параметром 'city' от неавторизованных пользователей"
                        f"возвращаются без ошибок."
                    ),
                )

    def test_places_is_paginated(self):
        """Looks for fields that should be in paginated responses"""
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user=user)

        response = client.get(PLACES).data

        self.assertTrue("count" in response)
        self.assertTrue("next" in response)
        self.assertTrue("previous" in response)
        self.assertTrue("results" in response)

    def test_places_correct_fields_unauthorized_client(self):
        client = ViewPlacesTests.unauthorized_client
        query_param = {"city": ViewPlacesTests.city.id}

        response = client.get(PLACES, query_param).data

        fields = [
            "id",
            "info",
            "tags",
            "chosen",
            "title",
            "city",
            "address",
            "description",
            "link",
            "image_url",
        ]
        results = response.get("results")[0]
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in results, msg=f"Нет поля {field}")

    def test_places_correct_fields_authorized_client(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)

        response = client.get(PLACES).data

        fields = [
            "id",
            "info",
            "tags",
            "chosen",
            "title",
            "address",
            "city",
            "description",
            "link",
            "image_url",
        ]
        results = response.get("results")[0]
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in results, msg=f"Нет поля {field}")

    def test_duplicate_place_for_city_cannot_be_created(self):
        """Error should return when try to post existed place."""
        user = ViewPlacesTests.mentor
        existed_place = PlaceFactory()
        client = self.return_authorized_user_client(user)

        data = {
            "activity_type": 1,
            "address": existed_place.address,
            "age": 25,
            "city": existed_place.city.id,
            "image_url": get_temporary_image(),
            "title": existed_place.address,
        }

        response = client.post(
            path=PLACES,
            data=data,
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=(
                "Проверьте, что при попытке создать событие с одинаковым "
                "адресом, названием и городом возвращается ошибка 400."
            ),
        )

    def test_places_list_context(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)

        response = client.get(PLACES).data
        self.assertEqual(response["count"], 10)

        results = response.get("results")[0]
        obj = Place.objects.get(pk=1)
        self.assertEqual(results["id"], obj.pk)
        # Поле инфо проверю отдельным методом
        # Теги тоже
        self.assertEqual(results["chosen"], obj.chosen)
        self.assertEqual(results["title"], obj.title)
        self.assertEqual(results["address"], obj.address)
        self.assertEqual(results["city"], obj.city.id)
        self.assertEqual(results["description"], obj.description)
        self.assertEqual(results["link"], obj.link)
        self.assertEqual(
            results["image_url"],
            "http://testserver/media/" + str(obj.image_url),
        )

    def test_places_info_field_context(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)

        PlaceFactory.create_batch(3)
        obj_non_gender = Place.objects.get(id=1)
        obj_non_gender.gender = None
        obj_non_gender.save()

        obj = Place.objects.get(id=3)
        response = client.get(PLACES).data
        results = response["results"]
        self.assertEqual(
            results[0]["info"],
            "{} лет. {} отдых".format(
                str(obj_non_gender.age),
                obj_non_gender.get_activity_type(obj_non_gender.activity_type),
            ),
        )
        self.assertEqual(
            results[2]["info"],
            "{}, {} лет. {} отдых".format(
                obj.get_gender(obj.gender),
                str(obj.age),
                obj.get_activity_type(obj.activity_type),
            ),
        )

    def test_places_tag_field_correct(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)
        tag = PlacesTagFactory(name="test", slug="test")
        PlaceFactory.create_batch(1)
        obj = Place.objects.get(pk=1)
        obj.tags.add(tag)
        obj.save()
        response = client.get(PLACES).data
        results = response["results"][0]["tags"][0]["name"]
        self.assertTrue(str(tag) in results)

    def test_places_post_unauthorized_client(self):
        image = get_temporary_image()
        client = ViewPlacesTests.unauthorized_client
        place = {
            "activity_type": 1,
            "title": "123",
            "address": "1234",
            "city": ViewPlacesTests.city.id,
            "description": "1235",
            "image_url": image,
        }
        response = client.post(
            path=PLACES,
            data=place,
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_places_post_authorized_client(self):
        user = ViewPlacesTests.mentor
        image = get_temporary_image()

        client = self.return_authorized_user_client(user)
        place = {
            "age": 10,
            "activity_type": 1,
            "title": "123",
            "address": "1234",
            "city": ViewPlacesTests.city.id,
            "description": "1235",
            "image_url": image,
        }
        response = client.post(
            path=PLACES,
            data=place,
            format="multipart",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=(
                "Убедитесь, что зарегистрированный пользователь может"
                "отправить рекомендацию"
            ),
        )

    def test_places_post_empty_data(self):
        user = ViewPlacesTests.mentor
        client = self.return_authorized_user_client(user)
        response = client.post(path=PLACES)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
