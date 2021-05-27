from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse

from common.factories import CityFactory
from users.factories import UserFactory
from afisha.factories import EventFactory


class ViewAfishaTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory(name="Воркута")
        cls.event = EventFactory(city=cls.city)
        
        cls.mentor = UserFactory(profile__role="mentor")
        cls.moderator_reg = UserFactory(profile__role="moderator_reg")
        cls.moderator_gen = UserFactory(profile__role="moderator_gen")
        cls.admin = UserFactory(
            profile__role="admin",
            profile__city=cls.city,
        )
        cls.unauthorized_client = APIClient()

        cls.path_events = reverse(
            "events-participants",
            
        )

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_unathozried_user_cant_book_event(self):
        client = self.unauthorized_client
        data = {"event": self.event.pk}

        response = client.post(
            "/api/v1/afisha/event-participants/",
            data,
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_admin_can_book_event(self):
        client = self.return_authorized_user_client(self.admin)
        data = {"event": self.event.pk}

        response = client.post(
            "/api/v1/afisha/event-participants/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
