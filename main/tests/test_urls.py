from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common.factories import CityFactory
from users.factories import UserFactory
from users.models import Profile


class StaticURLTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory.create(name="SomeCity")
        cls.mentor = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=cls.city,
        )
        cls.moderator_reg = UserFactory(
            profile__role=Profile.Role.MODERATOR_REG,
            profile__city=cls.city,
        )
        cls.moderator_gen = UserFactory(
            profile__role=Profile.Role.MODERATOR_GEN,
            profile__city=cls.city,
        )
        cls.admin = UserFactory(
            profile__role=Profile.Role.ADMIN,
            profile__city=cls.city,
        )
        cls.users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
        ]
        cls.unauthorized_client = APIClient()

        cls.path_main = reverse("main_page")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_main_unauthorized_client(self):
        client = StaticURLTests.unauthorized_client
        response = client.get(StaticURLTests.path_main)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=(
                f"Проверьте что неавторизованный пользователь имеет "
                f"доступ к '{StaticURLTests.path_main}'."
            ),
        )

    def test_main(self):
        for user in StaticURLTests.users:
            client = self.return_authorized_user_client(user=user)
            response = client.get(StaticURLTests.path_main)
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
                msg=(
                    f"Проверьте что пользователь с ролью "
                    f"'{user.profile.role}' "
                    f"имеет доступ к "
                    f"'{StaticURLTests.path_main}'."
                ),
            )
