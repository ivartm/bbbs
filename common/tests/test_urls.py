from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import tempfile
import shutil

from common.models import Meeting
from config.settings import base
from django.core.files.uploadedfile import SimpleUploadedFile

from common.factories import CityFactory
from places.factories import PlaceFactory, PlacesTagFactory
from users.factories import UserFactory
from users.models import Profile
from users.utils import get_tokens_for_user

MEETINGS_URL = "http://127.0.0.1:8000/api/v1/meetings/"
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


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        base.MEDIA_ROOT = tempfile.mkdtemp(dir=base.BASE_DIR)
        cls.UPLOADED = SimpleUploadedFile(
            name="small.gif", content=SMALL_GIF, content_type="image/gif"
        )
        cls.city = CityFactory(name=CITY_NAME)
        cls.user = UserFactory(
            profile__role=Profile.Role.MENTOR,
            profile__city=cls.city,
            password=PASSWORD,
        )
        cls.tag1 = PlacesTagFactory(name=TAG)
        cls.place1 = PlaceFactory(
            tags=[cls.tag1],
            city=cls.city,
        )
        cls.unauthorized_client = APIClient()
        cls.token = get_tokens_for_user(cls.user)
        cls.meeting = Meeting.objects.create(
            # image=cls.UPLOADED,
            user=cls.user,
            description=DESCRIPTION,
            smile=Meeting.GLAD,
            place=cls.place1,
            date="2001-01-01",
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Рекурсивно удаляем временную после завершения тестов
        shutil.rmtree(base.MEDIA_ROOT, ignore_errors=False)

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_mentor_get_meeting(self):
        """Test mentor get meeting"""
        client = self.return_authorized_user_client(self.user)
        response = client.get(MEETINGS_URL)
        print(MEETINGS_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=(f"response = {response.content} \n"),
        )

    def test_mentor_create_meeting(self):
        """Test mentor create meeting"""
        client = self.return_authorized_user_client(self.user)

        data = {
            "image": SMALL_GIF,
            "user": self.user.id,
            "description": DESCRIPTION,
            "smile": Meeting.GLAD,
            "place": self.place1.id,
            "date": "2020-10-10",
        }
        response = client.post(MEETINGS_URL, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=(f"response = {response.content} \n"),
        )
        # self.assertIn("refresh", response.data)
        # self.assertIn("access", response.data)
