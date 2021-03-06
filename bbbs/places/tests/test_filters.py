from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from bbbs.common.factories import CityFactory
from bbbs.places.factories import PlaceFactory, PlacesTagFactory
from bbbs.users.factories import UserFactory

PLACES_URL = reverse("places-list")


class FilterTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory()
        cls.other_city = CityFactory()
        cls.mentor = UserFactory(profile__city=cls.city)

        cls.tag_1 = PlacesTagFactory(name="tag1")
        cls.tag_2 = PlacesTagFactory(name="tag2")

        PlaceFactory.create_batch(
            10,
            tags=[cls.tag_1],
            city=cls.city,
            published=True,
            chosen=True,
        )
        PlaceFactory.create_batch(
            20,
            tags=[cls.tag_2],
            city=cls.other_city,
            published=True,
            chosen=True,
        )
        PlaceFactory.create_batch(
            40,
            tags=[cls.tag_2],
            city=cls.city,
            published=True,
            chosen=True,
        )

        cls.unauthorized_client = APIClient()

        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(user=cls.mentor)

    def test_unauthorized_user_city_query_param_is_required(self):
        """Unauthorized users with without city query param receive 422."""
        client = FilterTests.unauthorized_client
        response = client.get(PLACES_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            msg=(
                "Убедитесь, что неавторизованным пользователям без query"
                "параметра 'city' возвращается соответствующая ошибка."
            ),
        )

    def test_unauthorized_user_with_valid_city_query_receives_200(self):
        """Unauthorized users with valid city query param receive Ok."""
        query_part_url = f"?city={FilterTests.city.id}"

        client = FilterTests.unauthorized_client
        response = client.get(PLACES_URL + query_part_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=(
                "Убедитесь, что НЕавторизованные пользователе с query "
                "параметром существующего города НЕ получают ошибку."
            ),
        )

    def test_unauthorized_user_with_invalid_city_query_receives_404(self):
        """Returns 400 if there is no city matching city query param."""
        non_existent_city = 200
        query_part_url = f"?city={non_existent_city}"

        client = FilterTests.unauthorized_client
        response = client.get(PLACES_URL + query_part_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg=(
                "Неавторизованный пользователи при запросе без города в query"
                "параметрах должны получать ошибку 400."
            ),
        )

    def test_authorized_user_without_query_receives_200(self):
        """Authorized user haven't to use query param."""
        client = FilterTests.authorized_client
        response = client.get(PLACES_URL)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=(
                "Убедитесь, что запрос от авторизованного пользователя без "
                "query параметра города возвращает Ок."
            ),
        )

    def test_authorized_user_city_and_tag_filter(self):
        """Authorized user: result is filtered either by city and tags.

        'city' have to be taken from user.
        """
        client = FilterTests.authorized_client

        query_part_url = "?tag=tag1"
        response_data = client.get(PLACES_URL + query_part_url).data
        count = response_data.get("count")
        self.assertEqual(
            count,
            10,
            msg=(
                "Авторизованный пользователь: проверьте фильтрацию по одному "
                "тэгу. Должна быть фильтрация по городу + тэгу."
            ),
        )

        query_part_url = "?tag=tag1&tag=tag2"
        response_data = client.get(PLACES_URL + query_part_url).data
        count = response_data.get("count")
        self.assertEqual(
            count,
            50,
            msg=(
                "Авторизованный пользователь: проверьте фильтрацию по 2 тэгам."
                "В выборку не должны попадать другие города."
            ),
        )

    def test_unauthorized_user_city_and_tag_filter(self):
        """Unauthorized user: result is filtered either by city and tags.

        'city' have to be taken from query param.
        """
        client = FilterTests.unauthorized_client

        city_id = FilterTests.city.id
        query_part_url = f"?tag=tag1&city={city_id}"
        response_data = client.get(PLACES_URL + query_part_url).data
        count = response_data.get("count")
        self.assertEqual(
            count,
            10,
            msg=(
                "Аноним: проверьте фильтрацию по одному "
                "тэгу. Должна быть фильтрация по городу + тэгу."
            ),
        )

        query_part_url = f"?tag=tag1&tag=tag2&city={city_id}"
        client = FilterTests.authorized_client
        response_data = client.get(PLACES_URL + query_part_url).data
        count = response_data.get("count")
        self.assertEqual(
            count,
            50,
            msg=(
                "Аноним: проверьте фильтрацию по 2 тэгам."
                "В выборку не должны попадать другие города."
            ),
        )

    def test_unpublished_place_should_not_be_listed(self):
        """
        Unpublished places should not be counted.
        It counts places in city, after it creates once more unpublished place
        and counts againg. The amount should be the same.
        """
        client = FilterTests.authorized_client

        response_data = client.get(PLACES_URL).data
        places_amount_before_creating = response_data.get("count")

        PlaceFactory(
            city=FilterTests.mentor.profile.city,
            published=False,
        )

        response_data = client.get(PLACES_URL).data
        places_amount_after_creating = response_data.get("count")

        self.assertEqual(
            places_amount_before_creating,
            places_amount_after_creating,
            msg="Неопубликованные места должны отсутствовать в списке.",
        )

    def test_authorized_user_chosen_is_true_filter(self):
        """Result should have only places with 'chosen=True' field."""
        PlaceFactory.create_batch(
            10,
            city=FilterTests.mentor.profile.city,
            published=True,
            chosen=False,
        )
        query_param = {"chosen": True}
        client = FilterTests.authorized_client

        response_data = client.get(PLACES_URL, query_param).data
        count = response_data.get("count")

        self.assertEqual(
            count,
            50,
            msg=(
                "Фильтр 'chosen=True' должен отдавать только места"
                "с этим флагом."
            ),
        )

    def test_authorized_user_chosen_is_false_filter(self):
        """Result should have only places with 'chosen=False' field."""
        PlaceFactory.create_batch(
            10,
            city=FilterTests.mentor.profile.city,
            published=True,
            chosen=False,
        )
        client = FilterTests.authorized_client
        query_param = {"chosen": False}

        response_data = client.get(PLACES_URL, query_param).data
        count = response_data.get("count")

        self.assertEqual(
            count,
            10,
            msg=(
                "Фильтр 'chosen=False' должен отдавать только места с этим"
                "флагом."
            ),
        )
