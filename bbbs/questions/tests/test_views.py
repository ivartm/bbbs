from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from bbbs.common.factories import CityFactory
from bbbs.questions.factories import QuestionFactoryWithoutAnswer
from bbbs.questions.models import Question
from bbbs.users.factories import UserFactory
from bbbs.users.models import Profile


class ViewQuestionsTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory(name="Ронг-Ченг")
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
        cls.unauthorized_client = APIClient()

        cls.authorized_users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
        ]

        cls.all_users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
            cls.unauthorized_client,
        ]

        cls.valid_question = "Very exciting question about the project."
        cls.empty_question = ""
        cls.short_question = "Short question."

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
        question = Question.objects.get(question=data["question"])
        expected_data = {
            "id": question.id,
            "tags": [],
            "answer": question.answer,
            "pub_date": question.pub_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "question": question.question,
        }
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
        for user in self.authorized_users:
            with self.subTest(user=user):
                client = self.return_authorized_user_client(user)
                data = {"question": self.valid_question + str(user)}
                response = client.post(
                    path=ViewQuestionsTests.path_questions,
                    data=data,
                    format="json",
                )
                question = Question.objects.get(question=data["question"])
                expected_data = {
                    "id": question.id,
                    "tags": [],
                    "answer": question.answer,
                    "pub_date": question.pub_date.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "question": question.question,
                }
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
        for user in self.all_users:
            with self.subTest(user=user):
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
                    text="Вопрос с таким Вопрос уже существует.",
                    msg_prefix=(
                        "Проверьте, что пользователь не может задать вопрос, "
                        "который уже есть в базе."
                    ),
                )

    def test_empty_question(self):
        for user in self.all_users:
            with self.subTest(user=user):
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
                    text="Это поле не может быть пустым.",
                    msg_prefix=(
                        "Проверьте, что пользователь не может "
                        "отправить запрос без вопроса."
                    ),
                )

    def test_short_question(self):
        for user in self.all_users:
            with self.subTest(user=user):
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
                        "Проверьте, что пользователь не может "
                        "задать очень короткий вопрос."
                    ),
                )
