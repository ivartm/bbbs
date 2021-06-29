from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common.factories import CityFactory
from places.factories import PlaceFactory, PlacesTagFactory
from users.factories import UserFactory

PLACES_URL = reverse("places")


class FilterTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory()
        cls.mentor = UserFactory()

        cls.tag = PlacesTagFactory()
        cls.place = PlaceFactory.create_batch(10)

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
        """Returns 404 if there is no city matching city query param."""
        non_existent_city = 200
        query_part_url = f"?city={non_existent_city}"

        client = FilterTests.unauthorized_client
        response = client.get(PLACES_URL + query_part_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            msg="Убедитесь, что если города нет возвращается ошибка 404.",
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
