from django.contrib.admin import AdminSite
from django.contrib.sites.models import Site
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from users.admin import UserAdmin
from users.models import Profile, User

TOKEN_URL = reverse('token')
REFRESH_URL = reverse('token_refresh')
PROFILE_URL = reverse('profile')
USERNAME = 'user@mail.ru'
PASSWORD = 'test'
SITE_NAME = 'Site'
DOMAIN = '127.0.0.1:8000'


class OurRequest(object):
    def __init__(self, user=None):
        self.user = user


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.site = Site(
            id=1, name=SITE_NAME,
            domain=DOMAIN
        )
        cls.site.save()
        cls.userAdminSite = UserAdmin(model=User, admin_site=AdminSite())

    def setUp(self):
        self.authorized_client = Client()
        self.user = User.objects.create_user(
            username=USERNAME,
            email=USERNAME,
            password=PASSWORD,
        )
        self.authorized_client.force_login(self.user)

    def test_api_token_for_mentor(self):
        """Test api token/ for mentor"""
        data = {
            "username": USERNAME,
            "password": PASSWORD,
        }
        response = self.client.post(TOKEN_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_api_token_for_not_mentor(self):
        """Test api token/ for not mentor"""
        userAdminSite = self.userAdminSite
        user = self.user
        roles = [
            Profile.Role.ADMIN,
            Profile.Role.MODERATOR_REG,
            Profile.Role.MODERATOR_GEN,
        ]
        for role in roles:
            user.profile.role = role
            userAdminSite.save_model(
                obj=user,
                request=OurRequest(user=user),
                form=UserAdmin.form,
                change=True
            )
            data = {
                "username": USERNAME,
                "password": PASSWORD,
            }
            response = self.client.post(TOKEN_URL, data, format='json')
            self.assertEqual(user.profile.role, role)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_refresh(self):
        """Test api token refresh"""
        data = {
            "username": USERNAME,
            "password": PASSWORD,
        }
        response = self.client.post(TOKEN_URL, data, format='json')
        refresh = response.data["refresh"]
        data = {
            "refresh": refresh,
        }
        response = self.client.post(REFRESH_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
