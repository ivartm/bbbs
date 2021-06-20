from django.contrib.admin import AdminSite
from django.test import TestCase

from afisha.models import User
from common.models import City
from users.admin import UserAdmin
from users.models import Profile

USERNAME = "user@mail.ru"
USERNAME_SUPERUSER = "superr@mail.ru"
NEW_USERNAME = "new_user@mail.ru"
CITY = "Москва"


class OurRequest(object):
    def __init__(self, user=None):
        self.user = user


class UsersCreateTests(TestCase):
    def setUp(self):
        self.city = City.objects.create(name=CITY, isPrimary=1)
        self.user = User.objects.create_user(
            username=USERNAME,
            email=USERNAME,
        )
        self.user_superuser = User.objects.create_superuser(
            username=USERNAME_SUPERUSER,
        )
        self.userAdminSite = UserAdmin(model=User, admin_site=AdminSite())

    def test_create_superuser(self):
        """Test create superuser."""
        user = self.user_superuser

        self.assertEqual(user.username, USERNAME_SUPERUSER)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.profile.role, Profile.Role.ADMIN)

    def test_create_user(self):
        """Test for creating a user on the admin site."""
        user = self.user_superuser
        
        userAdminSite = self.userAdminSite
        userAdminSite.save_model(
            obj=User(username=NEW_USERNAME, email=NEW_USERNAME),
            request=OurRequest(user=user),
            form=UserAdmin.form,
            change=False,
        )
        user_new = User.objects.get(username=NEW_USERNAME)
        user_new.profile.city = self.city
        self.assertEqual(user_new.username, NEW_USERNAME)
        self.assertEqual(user_new.profile.role, Profile.Role.MENTOR)
        self.assertEqual(user_new.profile.city, self.city)
        self.assertTrue(user_new.is_active)
        self.assertFalse(user_new.is_staff)
        self.assertFalse(user_new.is_superuser)

    def test_create_admin(self):
        """Test for changing role (admin) on the admin site."""
        userAdminSite = UserAdmin(model=User, admin_site=AdminSite())
        user = self.user

        self.assertEqual(user.profile.role, Profile.Role.MENTOR)
        user.profile.role = Profile.Role.ADMIN
        userAdminSite.save_model(
            obj=user,
            request=OurRequest(user=user),
            form=UserAdmin.form,
            change=True,
        )
        user.profile.save() # В тестах как будто не сохраняем форму с профилем

        self.assertEqual(user.username, USERNAME)
        self.assertEqual(user.profile.role, Profile.Role.ADMIN)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_moderator_general(self):
        """Test for changing role (moderator general) on the admin site"""
        user = self.user
        userAdminSite = self.userAdminSite
        user.profile.role = Profile.Role.MODERATOR_GEN

        userAdminSite.save_model(
            obj=user,
            request=OurRequest(user=user),
            form=UserAdmin.form,
            change=True,
        )
        user.profile.save() # В тестах как будто не сохраняем форму с профилем

        self.assertEqual(user.username, USERNAME)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.profile.role, Profile.Role.MODERATOR_GEN)

    def test_create_moderator_regional(self):
        """Test for changing role (moderator regional) on the admin site."""
        user = self.user
        userAdminSite = self.userAdminSite
        user.profile.role = Profile.Role.MODERATOR_REG

        userAdminSite.save_model(
            obj=user,
            request=OurRequest(user=user),
            form=UserAdmin.form,
            change=True,
        )
        user.profile.save() # В тестах как будто не сохраняем форму с профилем

        self.assertEqual(user.username, USERNAME)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.profile.role, Profile.Role.MODERATOR_REG)

    def test_create_mentor(self):
        """Test for changing role (mentor) on the admin site."""
        user = self.user
        userAdminSite = self.userAdminSite
        user.profile.role = Profile.Role.MENTOR

        userAdminSite.save_model(
            obj=user,
            request=OurRequest(user=user),
            form=UserAdmin.form,
            change=True,
        )
        self.assertEqual(user.username, USERNAME)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.profile.role, Profile.Role.MENTOR)
