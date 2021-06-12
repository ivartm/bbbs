from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from common.factories import CityFactory
from users.factories import UserFactory


class StaticURLTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory.create(name="Ронг-Ченг")
        cls.mentor = UserFactory.create(
            profile__role="mentor",
            profile__city=cls.city,
        )
        cls.moderator_reg = UserFactory.create(
            profile__role="moderator_reg",
            profile__city=cls.city,
        )
        cls.moderator_gen = UserFactory.create(
            profile__role="moderator_gen",
            profile__city=cls.city,
        )
        cls.admin = UserFactory.create(
            profile__role="admin",
            profile__city=cls.city,
        )
        cls.users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
        ]
        cls.unauthorized_client = APIClient(

        )

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
        for man in range(len(self.users)):
            user = StaticURLTests.users[man]
            client = self.return_authorized_user_client(user=user)
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
        for man in range(len(self.users)):
            user = StaticURLTests.users[man]
            client = self.return_authorized_user_client(user=user)
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
