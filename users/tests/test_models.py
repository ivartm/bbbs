from django.contrib.auth import get_user_model
from django.test import TestCase

from common.factories import CityFactory
from users.models import Profile

User = get_user_model()


USERNAME = "user@mail.ru"
USERNAME_SUPERUSER = "superr@mail.ru"
NEW_USERNAME = "new_user@mail.ru"
CITY_NAME = "Москва"
CITY_2_NAME = "Мельбурн"


class UsersCreateTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory(name=CITY_NAME)
        cls.city_2 = CityFactory(name=CITY_2_NAME)

    def setUp(self):
        self.user = User.objects.create_user(
            username=USERNAME,
            email=USERNAME,
        )
        self.user_superuser = User.objects.create_superuser(
            username=USERNAME_SUPERUSER,
        )

    def test_create_superuser(self):
        """Test create superuser."""
        user = self.user_superuser
        self.assertEqual(user.profile.city, self.city)
        self.assertEqual(user.username, USERNAME_SUPERUSER)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.profile.role, Profile.Role.ADMIN)

    def test_create_user(self):
        """Test for creating user."""
        user = self.user
        user.profile.city = self.city

        self.assertEqual(user.username, USERNAME)
        self.assertEqual(user.profile.role, Profile.Role.MENTOR)
        self.assertEqual(user.profile.city, self.city)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_admin(self):
        """Test for changing role (admin) and city"""
        user = self.user
        user.profile.city = self.city_2
        user.profile.role = Profile.Role.ADMIN
        user.profile.save()

        self.assertEqual(user.username, USERNAME)
        self.assertEqual(user.profile.city, self.city_2)
        self.assertEqual(user.profile.role, Profile.Role.ADMIN)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_moderator_general(self):
        """Test for changing role (moderator general) and city"""
        user = self.user
        user.profile.city = self.city_2
        user.profile.role = Profile.Role.MODERATOR_GEN
        user.profile.save()

        self.assertEqual(user.profile.city, self.city_2)
        self.assertEqual(user.username, USERNAME)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.profile.role, Profile.Role.MODERATOR_GEN)

    def test_create_moderator_regional(self):
        """Test for changing role (moderator reg) and city, add regions."""
        user = self.user
        user.profile.role = Profile.Role.MODERATOR_REG
        user.profile.city = self.city_2
        user.profile.region.add(self.city, self.city_2)
        user.profile.save()

        self.assertEqual(user.username, USERNAME)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.profile.city, self.city_2)
        self.assertEqual(
            [self.city, self.city_2], list(user.profile.region.all())
        )
        self.assertEqual(user.profile.role, Profile.Role.MODERATOR_REG)

    def test_create_mentor(self):
        """Test for changing role (mentor) and city."""
        user = self.user_superuser
        user.profile.role = Profile.Role.MENTOR
        user.profile.city = self.city_2
        user.profile.save()

        self.assertEqual(user.profile.city, self.city_2)
        self.assertEqual(user.username, USERNAME_SUPERUSER)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.profile.role, Profile.Role.MENTOR)
