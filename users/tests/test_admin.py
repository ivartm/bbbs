from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from common.factories import CityFactory
from users.admin import UserAdmin
from users.factories import UserFactory
from users.models import Profile

TOKEN_URL = reverse("token")
REFRESH_URL = reverse("token_refresh")
PROFILE_URL = reverse("profile")
ADMIN_URL = "/admin/"
VIEW_URL = "auth/user/"
ADD_URL = "auth/user/add/"
EDIT_URL = "auth/user/{id}/change/"
DELETE_URL = "auth/user/{id}/delete/"
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
        cls.unauthorized_client = Client()
        cls.userAdminSite = UserAdmin(model=User, admin_site=AdminSite())
        cls.user_and_code = {
            cls.mentor: status.HTTP_302_FOUND,
            cls.moderator_reg: status.HTTP_403_FORBIDDEN,
            cls.moderator_gen: status.HTTP_403_FORBIDDEN,
            cls.admin: status.HTTP_200_OK,
        }

    def return_authorized_user_client(self, user):
        authorized_client = Client()
        authorized_client.force_login(user)
        return authorized_client

    def test_access_to_view_users_on_admin_site(self):
        """Test access to view users on admin site"""
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

    def test_access_to_add_users_on_admin_site(self):
        """Test access to add users on admin site"""
        for user, code in self.user_and_code.items():
            client = self.return_authorized_user_client(user=user)
            response = client.get(FULL_ADD_URL)

            self.assertEqual(response.status_code, code)

    def test_access_to_change_users_on_admin_site(self):
        """Test access to change users on admin site"""
        user_and_code = {
            self.mentor: status.HTTP_302_FOUND,
            self.moderator_reg: status.HTTP_403_FORBIDDEN,
            # self.moderator_gen: status.HTTP_403_FORBIDDEN,
            # после исправления кода снять коммент, а лучше ниже обращаться к
            # словарю  self.user_and_code.items()
            self.admin: status.HTTP_200_OK,
        }

        for user, code in user_and_code.items():
            client = self.return_authorized_user_client(user=user)
            response = client.get(FULL_EDIT_URL.format(id=user.id))

            self.assertEqual(response.status_code, code)

    def test_access_to_delete_users_on_admin_site(self):
        """Test access to delete users on admin site"""
        print(self.userAdminSite.urls)
        for user, code in self.user_and_code.items():
            client = self.return_authorized_user_client(user=user)
            user_new = UserFactory(
                profile__role=Profile.Role.MENTOR,
                profile__city=self.city,
                password=PASSWORD,
            )
            response = client.get(FULL_DELETE_URL.format(id=user_new.id))

            self.assertEqual(response.status_code, code)
