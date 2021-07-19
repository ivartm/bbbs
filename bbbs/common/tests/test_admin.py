from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from bbbs.common.factories import CityFactory
from bbbs.users.admin import UserAdmin
from bbbs.users.factories import UserFactory
from bbbs.users.models import Profile

TOKEN_URL = reverse("token")
REFRESH_URL = reverse("token_refresh")
PROFILE_URL = reverse("profile")
ADMIN_URL = "/admin/"
VIEW_URL = "common/city/"
ADD_URL = "common/city/add/"
EDIT_URL = "common/city/{id}/change/"
DELETE_URL = "common/city/{id}/delete/"
FULL_VIEW_URL = ADMIN_URL + VIEW_URL
FULL_ADD_URL = ADMIN_URL + ADD_URL
FULL_EDIT_URL = ADMIN_URL + EDIT_URL
FULL_DELETE_URL = ADMIN_URL + DELETE_URL


USERNAME = "user@mail.ru"
PASSWORD = "test"
SITE_NAME = "Site"
DOMAIN = "127.0.0.1:8000"
CITY_NAME = "Мельбурн"
CITY_NEW_NAME = "Нью-йорк"

User = get_user_model()


class PermissionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory(name=CITY_NAME)
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
        cls.unauthorized_client = Client()
        cls.userAdminSite = UserAdmin(model=User, admin_site=AdminSite())
        cls.user_and_code = {
            cls.mentor: status.HTTP_302_FOUND,
            cls.moderator_reg: status.HTTP_403_FORBIDDEN,
            cls.moderator_gen: status.HTTP_200_OK,
            cls.admin: status.HTTP_200_OK,
        }

    def return_authorized_user_client(self, user):
        authorized_client = Client()
        authorized_client.force_login(user)
        return authorized_client

    def test_access_to_view_city_on_admin_site(self):
        """Test access to view city on admin site"""
        user_and_code = {
            self.mentor: status.HTTP_302_FOUND,
            self.moderator_reg: status.HTTP_403_FORBIDDEN,
            self.moderator_gen: status.HTTP_200_OK,
            self.admin: status.HTTP_200_OK,
        }
        for user, code in user_and_code.items():
            client = self.return_authorized_user_client(user=user)
            response = client.get(FULL_VIEW_URL)

            self.assertEqual(response.status_code, code)

    def test_access_to_add_city_on_admin_site(self):
        """Test access to add city on admin site"""
        for user, code in self.user_and_code.items():
            client = self.return_authorized_user_client(user=user)
            response = client.get(FULL_ADD_URL)

            self.assertEqual(response.status_code, code)

    def test_access_to_change_city_on_admin_site(self):
        """Test access to change city on admin site"""

        user_and_code = {
            self.mentor: status.HTTP_302_FOUND,
            self.moderator_reg: status.HTTP_403_FORBIDDEN,
            self.moderator_gen: status.HTTP_302_FOUND,
            self.admin: status.HTTP_302_FOUND,
        }
        data = {"name": "Тест2", "_save": "Сохранить"}

        for user, code in user_and_code.items():
            client = self.return_authorized_user_client(user=user)
            response = client.post(
                FULL_EDIT_URL.format(id=self.city.id), data=data
            )

            self.assertEqual(response.status_code, code)

    def test_access_to_delete_city_on_admin_site(self):
        """Test access to delete city on admin site"""
        print(self.userAdminSite.urls)
        for user, code in self.user_and_code.items():
            city_new = CityFactory(name=CITY_NEW_NAME)
            client = self.return_authorized_user_client(user=user)
            response = client.post(FULL_DELETE_URL.format(id=city_new.id))
            self.assertEqual(response.status_code, code)
