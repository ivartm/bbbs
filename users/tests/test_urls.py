from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from common.factories import CityFactory
from users.factories import UserFactory
from users.models import Profile

TOKEN_URL = reverse("token")
REFRESH_URL = reverse("token_refresh")
PROFILE_URL = reverse("profile")
USERNAME = "user@mail.ru"
PASSWORD = "test"
SITE_NAME = "Site"
DOMAIN = "127.0.0.1:8000"
CITY_NAME = "Мельбурн"
CITY_NEW_NAME = "Нью-йорк"


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory(name=CITY_NAME)
        cls.city_new = CityFactory(name=CITY_NEW_NAME)
        cls.mentor = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=cls.city,
            password=PASSWORD,
        )
        cls.moderator_reg = UserFactory(
            profile__role=Profile.Role.MODERATOR_REG,
            profile__city=cls.city,
            password=PASSWORD,
        )
        cls.moderator_gen = UserFactory(
            profile__role=Profile.Role.MODERATOR_GEN,
            profile__city=cls.city,
            password=PASSWORD,
        )
        cls.admin = UserFactory(
            profile__role=Profile.Role.ADMIN,
            profile__city=cls.city,
            password=PASSWORD,
        )
        cls.staff_users = [
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
        ]
        cls.users = cls.staff_users + [cls.mentor]
        cls.unauthorized_client = APIClient()

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_api_token_for_mentor(self):
        """Test api token/ for mentor"""
        client = URLTests.unauthorized_client
        user = URLTests.mentor

        data = {
            "username": user.username,
            "password": PASSWORD,
        }
        response = client.post(TOKEN_URL, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=(
                f"response = {response.content} \n"
                f"user_role = {user.profile.role}"
            ),
        )
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_api_token_for_not_mentor(self):
        """Test api token/ for not mentor"""
        client = URLTests.unauthorized_client

        for user in URLTests.staff_users:
            with self.subTest(user=user):
                data = {
                    "username": user.username,
                    "password": PASSWORD,
                }
                response = client.post(TOKEN_URL, data, format="json")

                self.assertContains(
                    response,
                    status_code=400,
                    text="Ошибка прав доступа.",
                    msg_prefix=(
                        f"Проверьте, что пользователь с правами "
                        f"'{user.profile.role}'не может получить "
                        f"токен. Ответ: {response.content}"
                    ),
                )

    def test_token_refresh(self):
        """Test api token refresh"""
        client = URLTests.unauthorized_client
        user = URLTests.mentor
        data = {
            "username": user.username,
            "password": PASSWORD,
        }

        response = client.post(TOKEN_URL, data, format="json")
        refresh = response.data["refresh"]
        data = {
            "refresh": refresh,
        }

        response = self.client.post(REFRESH_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_profile_get(self):
        """Test api get profile"""
        user = URLTests.mentor
        expected_data = {
            "id": user.profile.id,
            "user": user.id,
            "city": {
                "id": user.profile.city.id,
                "name": user.profile.city.name,
                "is_primary": user.profile.city.is_primary,
            },
        }
        client = self.return_authorized_user_client(user=user)

        response = client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_profile_patch(self):
        """Test api patch profile (change city)"""
        user = URLTests.mentor
        data = {
            "id": user.profile.id,
            "user": user.id,
            "city": self.city_new.id,
        }
        client = self.return_authorized_user_client(user=user)

        response = client.patch(PROFILE_URL, data=data)
        data_response = {
            "id": user.profile.id,
            "user": user.id,
            "city": {
                "id": self.city_new.id,
                "name": self.city_new.name,
                "is_primary": self.city_new.is_primary,
            },
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data_response)

    def test_profile_put(self):
        """Test api put profile (change city)"""
        user = URLTests.mentor
        data = {
            "id": user.profile.id,
            "user": user.id,
            "city": self.city_new.id,
        }
        client = self.return_authorized_user_client(user=user)

        response = client.put(PROFILE_URL, data=data)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_profile_delete(self):
        """Test api delete profile"""
        user = URLTests.mentor
        data = {
            "id": user.profile.id,
        }
        client = self.return_authorized_user_client(user=user)

        response = client.delete(PROFILE_URL, data=data)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
