from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from common.factories import CityFactory
from questions.factories import QuestionFactoryWithoutAnswer
from questions.tests.test_urls import StaticURLTests
from users.factories import UserFactory


class ViewQuestionsTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
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

        cls.valid_question = "Very exciting question about the project."
        cls.empty_question = ""
        cls.short_question = "Short question."

        cls.unauthorized_client = APIClient()

        cls.path_questions = reverse("questions")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_unauthorized_user_can_ask_question(self):
        client = ViewQuestionsTests.unauthorized_client
        data = {"question": self.valid_question}
        response = client.post(
            path=ViewQuestionsTests.path_questions, data=data, format="json"
        )
        expected_data = {"Success": "Спасибо! Мы приняли ваш вопрос."}
        self.assertEqual(
            response.status_code,
            201,
            msg=(
                "Проверьте, что при успешном добавлении вопроса "
                "возвращается статус 201."
            ),
        )
        self.assertEqual(
            response.data,
            expected_data,
            msg=("Проверьте, что возвращается правильный JSON."),
        )

    def test_authorized_user_can_ask_question(self):
        for man in range(len(self.users)):
            user = StaticURLTests.users[man]
            client = self.return_authorized_user_client(user=user)
            data = {"question": self.valid_question + str(man)}
            response = client.post(
                path=ViewQuestionsTests.path_questions,
                data=data,
                format="json",
            )
            expected_data = {"Success": "Спасибо! Мы приняли ваш вопрос."}
            self.assertEqual(
                response.status_code,
                201,
                msg=(
                    f"Проверьте у пользователя с ролью "
                    f"'{user.profile.role}' "
                    f"возвращается статус 201."
                ),
            )
            self.assertEqual(
                response.data,
                expected_data,
                msg=("Проверьте, что возвращается правильный JSON."),
            )

    def test_duplicate_question(self):
        user = ViewQuestionsTests.mentor
        question = QuestionFactoryWithoutAnswer.create()
        client = self.return_authorized_user_client(user)
        data = data = {"question": question.question}
        response = client.post(
            path=ViewQuestionsTests.path_questions,
            data=data,
            format="json",
        )
        self.assertContains(
            response,
            status_code=400,
            text="Такой вопрос уже задавали",
            msg_prefix=(
                "Проверьте, что пользователь не может задать вопрос,",
                "который уже есть в базе."
            ),
        )

    def test_empty_question(self):
        user = ViewQuestionsTests.mentor
        client = self.return_authorized_user_client(user)
        data = data = {"question": self.empty_question}
        response = client.post(
            path=ViewQuestionsTests.path_questions,
            data=data,
            format="json",
        )
        self.assertContains(
            response,
            status_code=400,
            text="Пожалуйста, введите вопрос",
            msg_prefix=(
                "Проверьте, что пользователь не может",
                "отправить запрос без вопроса."
            ),
        )

    def test_short_question(self):
        user = ViewQuestionsTests.mentor
        client = self.return_authorized_user_client(user)
        data = data = {"question": self.short_question}
        response = client.post(
            path=ViewQuestionsTests.path_questions,
            data=data,
            format="json",
        )
        self.assertContains(
            response,
            status_code=400,
            text="Задайте более развёрнутый вопрос",
            msg_prefix=(
                "Проверьте, что пользователь не может",
                "задать очень короткий вопрос."
            ),
        )
