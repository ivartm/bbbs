from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse
from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from users.factories import UserFactory
from common.factories import CityFactory

class AdminURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory(name="Воркута")
        cls.mentor = UserFactory(
            profile__role="mentor",
            profile__city=cls.city,
        )
        cls.moderator_reg = UserFactory(
            profile__role="moderator_reg",
            profile__city=cls.city,
        )
        cls.moderator_gen = UserFactory(
            profile__role="moderator_gen",
            profile__city=cls.city,
        )
        cls.admin = UserFactory(
            profile__role="admin",
            profile__city=cls.city,
        )
        cls.users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
        ]
        cls.admin_pages = {
            "/admin/",
            "/admin/auth/",
            "/admin/auth/group/",
            "/admin/auth/group/add/",
            "/admin/auth/user/",
            "/admin/auth/user/add/",
            "/admin/password_change/",
            "/admin/common/",
            "/admin/common/city/",
            "/admin/common/city/add/",
            # f"/admin/common/city/{pk.city}/change/",
            # f"/admin/common/city/{pk.city}/delete/",
            # "/admin/afisha/",
            # "/admin/afisha/event/",
            # f"/admin/afisha/event/{pk.event}/change/",
            # f"/admin/afisha/event/{pk.event}/delete/"

        }

    def setUp(self):
        self.site = AdminSite()
        self.guest_client = Client()
        mentor = self.mentor
        moderator_reg = self.moderator_reg
        moderator_gen = self.moderator_gen
        admin = self.admin
        self.client_mentor = Client()
        self.client_moderator_reg = Client()
        self.client_moderator_gen = Client()
        self.client_admin = Client()
        self.client_mentor.force_login(mentor)
        self.client_moderator_reg.force_login(moderator_reg)
        self.client_moderator_gen.force_login(moderator_gen)
        self.client_admin.force_login(admin)

    def test_url_access(self):
        response = self.client_admin.get("/admin/auth/")
        self.assertEqual(response.status_code, 200)