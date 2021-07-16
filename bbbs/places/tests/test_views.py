from tempfile import mkdtemp as tempfile_mkdtemp

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, override_settings

from bbbs.common.factories import CityFactory
from bbbs.places.factories import PlaceFactory, PlacesTagFactory
from bbbs.users.factories import UserFactory
from bbbs.users.models import Profile

PLACES = reverse("places-list")
PLACES_TAGS = reverse("places-tags")
PLACES_MAIN = reverse("places-main")

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
        PlaceFactory.create_batch(
            10,
            city=cls.city,
            published=True,
        )
        cls.unauthorized_client = APIClient()

        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(user=cls.mentor)

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
        client = ViewPlacesTests.authorized_client

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
        client = ViewPlacesTests.authorized_client

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
        existed_place = PlaceFactory()
        client = ViewPlacesTests.authorized_client
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

    def test_places_list_ordering(self):
        """Last created place should be first."""
        mentor = ViewPlacesTests.mentor
        last_place = PlaceFactory(
            city=mentor.profile.city,
            published=True,
        )
        client = ViewPlacesTests.authorized_client

        response_data = client.get(PLACES).data
        result = response_data.get("results")[0]

        self.assertEqual(
            result["id"],
            last_place.pk,
            msg="Последнее опубликованное место должно быть первым в списке.",
        )

    def test_places_info_filed_non_gender(self):
        """Comparing 'info' field in place without gender."""
        mentor = ViewPlacesTests.mentor
        PlaceFactory(
            city=mentor.profile.city,
            gender=None,
            age=10,
            activity_type=1,
            published=True,
        )
        expected_info = "10 лет. Развлекательный отдых"

        client = ViewPlacesTests.authorized_client
        response_data = client.get(PLACES).data
        result = response_data["results"][0]

        self.assertEqual(
            result["info"],
            expected_info,
            msg=(
                "Когда не задан пол, информация о месте должна выглядеть"
                "как в примере."
            ),
        )

    def test_places_info_filed_male_gender(self):
        """Comparing 'info' field in place with Male gender."""
        mentor = ViewPlacesTests.mentor
        PlaceFactory(
            city=mentor.profile.city,
            gender="M",
            age=16,
            activity_type=0,
            published=True,
        )
        expected_info = "Мальчик, 16 лет. Активный отдых"
        client = ViewPlacesTests.authorized_client

        response_data = client.get(PLACES).data
        result = response_data["results"][0]

        self.assertEqual(
            result["info"],
            expected_info,
            msg=(
                "Когда у места задан пол ребенка, информация должна выглядеть"
                "как в примере."
            ),
        )

    def test_places_tag_field_correct(self):
        client = ViewPlacesTests.authorized_client
        tag = PlacesTagFactory(name="test", slug="test")
        PlaceFactory(
            published=True,
            tags=[tag],
            city=ViewPlacesTests.city,
        )

        response_data = client.get(PLACES).data
        results = response_data.get("results")[0]["tags"][0]["name"]

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
        image = get_temporary_image()

        client = ViewPlacesTests.authorized_client
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
        client = ViewPlacesTests.authorized_client
        response = client.post(path=PLACES)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_places_main_returns_last_place(self):
        """
        Should return last published place with 'chosen=True' in the city.
        """
        PlaceFactory(  # previous_place
            city=ViewPlacesTests.city,
            published=True,
            chosen=True,
        )
        last_place = PlaceFactory(
            city=ViewPlacesTests.city, published=True, chosen=True
        )
        client = ViewPlacesTests.authorized_client

        response_data = client.get(PLACES_MAIN).data
        place_id = response_data.get("id")

        self.assertEqual(
            place_id,
            last_place.id,
            msg=(
                "В main должен возвращаться последний опубликованный"
                "объект. Не предыдущий."
            ),
        )

    def test_places_main_returns_last_place_with_chosen_true(self):
        """Should return last place with 'chosen=True'."""
        chosen_place = PlaceFactory(
            city=ViewPlacesTests.city, published=True, chosen=True
        )
        PlaceFactory(  # not chosen place
            city=ViewPlacesTests.city, published=True, chosen=False
        )
        client = ViewPlacesTests.authorized_client

        response_data = client.get(PLACES_MAIN).data
        place_id = response_data.get("id")

        self.assertEqual(
            place_id,
            chosen_place.id,
            msg=(
                "В main должен возвращаться последний опубликованный"
                "объект с атрибутом 'chosen=True'"
            ),
        )

    def test_places_main_returns_last_chosen_place_in_city(self):
        """Should return last place with 'chosen=True' in the city."""
        other_city = CityFactory()
        place_in_city = PlaceFactory(
            city=ViewPlacesTests.city,
            published=True,
            chosen=True,
        )
        PlaceFactory(  # place in other city
            city=other_city,
            published=True,
            chosen=True,
        )
        client = ViewPlacesTests.authorized_client

        response_data = client.get(PLACES_MAIN).data
        place_id = response_data.get("id")

        self.assertEqual(
            place_id,
            place_in_city.id,
            msg="В main должен возвращаться последний объект в городе.",
        )

    def test_places_main_returns_last_place_if_there_is_no_chosen(self):
        """
        If there is no 'chosen=True' places in the city it should return
        last 'place' in the city.
        """
        city = CityFactory()
        mentor = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=city,
        )
        PlaceFactory.create_batch(  # previous not chosen places
            10,
            city=city,
            published=True,
            chosen=False,
        )
        last_not_chosen_place = PlaceFactory(
            city=city,
            published=True,
            chosen=False,
        )
        client = APIClient()
        client.force_authenticate(user=mentor)

        response_data = client.get(PLACES_MAIN).data
        place_id = response_data.get("id")

        self.assertEqual(
            place_id,
            last_not_chosen_place.id,
            msg=(
                "Если нет места с 'chosen=True' должно возвращаться"
                "последнее."
            ),
        )

    def test_places_main_returns_empty_list_if_no_places(self):
        """If there is no places in city should return []."""
        city = CityFactory()
        mentor = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=city,
        )
        client = APIClient()
        client.force_authenticate(user=mentor)

        response = client.get(PLACES_MAIN)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [],
            msg="Если нет событий в городе возвращать пустой список.",
        )
