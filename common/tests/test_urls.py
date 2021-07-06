import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from common.factories import CityFactory
from common.models import Meeting
from config.settings import base
from users.factories import UserFactory
from users.models import Profile

MEETINGS_URL = "/api/v1/meetings/"
MEETING_URL = "/api/v1/meetings/{id}/"
PASSWORD = "test"
CITY_NAME = "Мельбурн"
SMALL_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00"
    b"\x01\x00\x00\x00\x00\x21\xf9\x04"
    b"\x01\x0a\x00\x01\x00\x2c\x00\x00"
    b"\x00\x00\x01\x00\x01\x00\x00\x02"
    b"\x02\x4c\x01\x00\x3b"
)
DESCRIPTION = "Test"
TAG = "tag"
URL_IMAGE = "meetings/small.gif"
DATA = "2020-10-10"
PLACE = "Test"
PLACE2 = "Test2"


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        base.MEDIA_ROOT = tempfile.mkdtemp(dir=base.BASE_DIR)
        cls.city = CityFactory(name=CITY_NAME)
        cls.user = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=cls.city,
            password=PASSWORD,
        )
        cls.user2 = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=cls.city,
            password=PASSWORD,
        )
        cls.UPLOADED = SimpleUploadedFile(
            name="small.gif", content=SMALL_GIF, content_type="image/gif"
        )
        cls.unauthorized_client = APIClient()

    def setUp(self):
        self.meeting = Meeting.objects.create(
            image=self.UPLOADED,
            user=self.user,
            description=DESCRIPTION,
            smile=Meeting.GLAD,
            place=PLACE,
            date=DATA,
        )
        self.meeting2 = Meeting.objects.create(
            image=self.UPLOADED,
            user=self.user2,
            description=DESCRIPTION,
            smile=Meeting.GLAD,
            place=PLACE2,
            date=DATA,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Рекурсивно удаляем временную после завершения тестов
        shutil.rmtree(base.MEDIA_ROOT, ignore_errors=False)

    def url_returns_401_unauthorized_test_utility(
        self, client, url, method_names
    ):
        """Helper. Tests "url" for not allowed methods.

        It translates "methods_names" to correspond methods on "client" and
        asserts when error different from 401 (UNAUTHORIZED) returns.
        """

        for method_name in method_names:
            with self.subTest(method_name):
                method = getattr(client, method_name)
                response = method(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED,
                    msg=(
                        f"Убедитесь, что для '{url}' "
                        f"метод '{method_name}' запрещен и возвращает "
                        f"правильный номер ошибки."
                    ),
                )

    def url_returns_404_not_found_test_utility(
        self, client, url, method_names
    ):
        """Helper. Tests "url" for not allowed methods.

        It translates "methods_names" to correspond methods on "client" and
        asserts when error different from 404 (not found) returns.
        """

        for method_name in method_names:
            with self.subTest(method_name):
                method = getattr(client, method_name)
                response = method(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_404_NOT_FOUND,
                    msg=(
                        f"Убедитесь, что для '{url}' "
                        f"метод '{method_name}' запрещен и возвращает "
                        f"правильный номер ошибки."
                    ),
                )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_mentor_get_list_meeting(self):
        """Test mentor get list meeting"""
        client = self.return_authorized_user_client(self.user)
        response = client.get(MEETINGS_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=(f"response = {response.content} \n"),
        )
        self.assertEqual(
            response.data["count"],
            Meeting.objects.filter(user=self.user).count(),
        )

    def test_mentor_get_meeting(self):
        """Test mentor get meeting"""
        client = self.return_authorized_user_client(self.user)
        response = client.get(MEETING_URL.format(id=self.meeting.id))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"response = {response.content} \n",
        )
        self.assertEqual(response.data["user"], self.meeting.user.id)
        self.assertEqual(
            response.data["description"], self.meeting.description
        )
        self.assertEqual(response.data["smile"], self.meeting.smile)
        self.assertEqual(response.data["place"], self.meeting.place)
        self.assertEqual(response.data["date"], self.meeting.date)

    def test_mentor_delete_meeting(self):
        """Test mentor delete meeting"""
        client = self.return_authorized_user_client(self.user)
        response = client.delete(MEETING_URL.format(id=self.meeting.id))
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg=f"response = {response.content} \n",
        )

    def test_mentor_create_meeting(self):
        """Test mentor create meeting"""
        client = self.return_authorized_user_client(self.user)

        data = {
            "user": self.user.id,
            "description": DESCRIPTION,
            "smile": Meeting.GLAD,
            "place": PLACE,
            "date": DATA,
        }
        files = self.UPLOADED
        response = client.post(
            MEETINGS_URL, data=data, files=files, format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=(f"response = {response.content} \n"),
        )
        self.assertEqual(response.data["user"], data["user"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["smile"], data["smile"])
        self.assertEqual(response.data["place"], data["place"])
        self.assertEqual(response.data["date"], data["date"])

    def test_mentor_patch_meeting(self):
        """Test mentor patch meeting"""
        client = self.return_authorized_user_client(self.user)
        meeting_new = Meeting.objects.create(
            image=self.UPLOADED,
            user=self.user,
            description=DESCRIPTION,
            smile=Meeting.GLAD,
            place=PLACE,
            date=DATA,
        )

        data = {
            "description": "Test test",
        }
        response = client.patch(
            MEETING_URL.format(id=meeting_new.id), data=data, format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(meeting_new.description, data["description"])

    def test_all_methods_not_allowed_to_unauthorized_users(self):
        """All methods not allowed to unauthorized users"""
        client = self.unauthorized_client

        self.url_returns_401_unauthorized_test_utility(
            client=client,
            url=MEETINGS_URL,
            method_names=["post", "get"],
        )
        self.url_returns_401_unauthorized_test_utility(
            client=client,
            url=MEETING_URL.format(id=self.meeting.id),
            method_names=["get", "patch", "put", "delete"],
        )

    def test_all_methods_not_allowed_to_not_owner(self):
        """All methods not allowed to unauthorized users"""
        client = self.return_authorized_user_client(self.user2)

        self.url_returns_404_not_found_test_utility(
            client=client,
            url=MEETING_URL.format(id=self.meeting.id),
            method_names=["get", "patch", "put", "delete"],
        )

        response = client.get(MEETINGS_URL)
        for meeting in response.data["results"]:
            self.assertEqual(
                meeting["user"],
                self.user2.id,
            )
