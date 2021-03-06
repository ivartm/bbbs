from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from bbbs.common.factories import CityFactory
from bbbs.users.factories import UserFactory
from bbbs.users.models import Profile


class StaticURLTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory.create(name="Ронг-Ченг")
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

        cls.path_questions = reverse("questions")
        cls.path_questions_tags = reverse("questions-tags")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_questions_unauthorized_client(self):
        client = StaticURLTests.unauthorized_client
        response = client.get(StaticURLTests.path_questions)
        self.assertEqual(
            response.status_code,
            200,
            msg=(
                f"Проверьте что неавторизованный пользователь имеет "
                f"доступ к '{StaticURLTests.path_questions}'."
            ),
        )

    def test_questions_tags_unauthorized_client(self):
        client = StaticURLTests.unauthorized_client
        response = client.get(StaticURLTests.path_questions_tags)
        self.assertEqual(
            response.status_code,
            200,
            msg=(
                f"Проверьте что неавторизованный пользователь имеет доступ "
                f"к '{StaticURLTests.path_questions_tags}'."
            ),
        )

    def test_questions(self):
        for user in self.users:
            with self.subTest(user=user):
                client = self.return_authorized_user_client(user)
                response = client.get(StaticURLTests.path_questions)
                self.assertEqual(
                    response.status_code,
                    200,
                    msg=(
                        f"Проверьте что пользователь с ролью "
                        f"'{user.profile.role}' "
                        f"имеет доступ к "
                        f"'{StaticURLTests.path_questions}'."
                    ),
                )

    def test_questions_tags(self):
        for user in self.users:
            with self.subTest(user=user):
                client = self.return_authorized_user_client(user)
                response = client.get(StaticURLTests.path_questions_tags)
                self.assertEqual(
                    response.status_code,
                    200,
                    msg=(
                        f"Проверьте что пользователь с ролью "
                        f"'{user.profile.role}' "
                        f"имеет доступ к "
                        f"'{StaticURLTests.path_questions_tags}'."
                    ),
                )

    def test_page_not_found(self):
        client = StaticURLTests.unauthorized_client
        response = client.get("/unknown-point/")
        self.assertEqual(
            response.status_code,
            404,
            msg=(
                "Проверьте что ошибка 404 возвращается для несуществующих "
                "эндпоинтов."
            ),
        )
