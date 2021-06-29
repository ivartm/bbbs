from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from common.factories import CityFactory
from rights.factories import RightFactory, RightTagFactory
from users.factories import UserFactory


class ViewRightTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.tag1 = RightTagFactory(name="!Шляпа!")
        cls.tag2 = RightTagFactory(name="?Петровна?")
        cls.right = RightFactory(tags__num=2)

        cls.city = CityFactory(name="Билибино")
        cls.mentor = UserFactory()

        cls.unauthorized_client = APIClient()
        cls.path_rights = reverse("rights")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_response_is_paginated(self):
        """Just look for 'next', 'previous', 'result' keys in response."""
        client = ViewRightTests.unauthorized_client
        RightFactory.create_batch(200)

        response_data = client.get(path=self.path_rights).data

        self.assertTrue("next" in response_data)
        self.assertTrue("previous" in response_data)
        self.assertTrue("results" in response_data)

    def test_rights_has_correct_fields(self):
        """Result has all expected fields."""
        client = ViewRightTests.unauthorized_client
        fields = [
            "id",
            "tag",
            "title",
            "description",
            "text",
            "color",
            "imageUrl",
        ]
        response = client.get(ViewRightTests.path_rights).data
        results = response.get("results")[0]
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(field in results, msg=f"Нет поля {field}")

    def test_rights_has_no_more_than_expected_fields(self):
        """Result has no more than expected fields."""
        client = ViewRightTests.unauthorized_client
        expected_fields = [
            "id",
            "tag",
            "title",
            "description",
            "text",
            "color",
            "imageUrl",
        ]
        response = client.get(ViewRightTests.path_rights).data
        results = response.get("results")[0]
        for field in results:
            with self.subTest(field=field):
                self.assertTrue(
                    field in expected_fields,
                    msg=f"В в возвращенном объекте неожидаемое поле {field}",
                )

    def test_rights_filtering_by_two_tags_returns_right(self):
        """Create 20 Right obj with 2 tags and count them in response."""
        tag_1 = RightTagFactory(name="Tag1")
        tag_2 = RightTagFactory(name="Tag2")
        tag_3 = RightTagFactory(name="Tag3")
        RightFactory.create_batch(20, tags=[tag_1, tag_2])
        RightFactory.create_batch(20, tags=[tag_3])
        query_part_url = "?tag=tag1&tag=tag2"

        client = ViewRightTests.unauthorized_client
        response = client.get(ViewRightTests.path_rights + query_part_url).data
        count = response.get("count")

        self.assertEqual(
            count,
            20,
            msg=(
                "Убедитесь, что фильтрация по тегам возвращает только "
                "объекты c заданными тегами."
            ),
        )
