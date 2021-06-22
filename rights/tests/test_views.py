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
        cls.right = RightFactory(num_tags=2)

        cls.city = CityFactory(name="Билибино")
        cls.mentor = UserFactory()

        cls.unauthorized_client = APIClient()
        cls.path_rights = reverse("rights")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_rights_get_response_status_code(self):
        """Mentor has access to Right list."""
        user = ViewRightTests.mentor
        client = self.return_authorized_user_client(user)
        response = client.get(ViewRightTests.path_rights)
        self.assertEqual(response.status_code, 200)

    def test_response_is_paginated(self):
        """Just look for 'next', 'previous', 'result' keys in response."""
        user = ViewRightTests.mentor
        RightFactory.create_batch(200)
        client = self.return_authorized_user_client(user)

        response_data = client.get(path=self.path_rights).data

        self.assertTrue("next" in response_data)
        self.assertTrue("previous" in response_data)
        self.assertTrue("results" in response_data)

    def test_rights_has_correct_fields(self):
        """Result has all expected fields."""
        user = ViewRightTests.mentor
        client = self.return_authorized_user_client(user=user)
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
        user = ViewRightTests.mentor
        client = self.return_authorized_user_client(user=user)
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
