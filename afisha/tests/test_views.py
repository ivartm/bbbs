from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate
from rest_framework.test import APITestCase

from pprint import pprint


from afisha.factories import CityFactory, EventFactory, UserFactory


class ViewAfishaTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.mentor = UserFactory(profile__role="mentor")
        cls.moderator_reg = UserFactory(profile__role="moderator_reg")
        cls.moderator_gen = UserFactory(profile__role="moderator_gen")
        cls.admin = UserFactory(
            profile__role="admin",
            profile__city__name="Воркута",
        )

        cls.city = CityFactory(name="Воркута")
        cls.event = EventFactory(city__name="Воркута")
        cls.unauthorized_client = APIClient()

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
