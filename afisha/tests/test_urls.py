from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from afisha.factories import EventFactory
from afisha.models import EventParticipant
from common.factories import CityFactory
from users.factories import UserFactory
from users.models import Profile


class AfishaURLTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.city = CityFactory(name="Воркута")
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
        cls.event = EventFactory(
            city=cls.mentor.profile.city,
        )
        cls.booking = EventParticipant.objects.create(
            user=cls.mentor,
            event=cls.event,
        )

        cls.unauthorized_client = APIClient()
        cls.path_events_participants = reverse("event-participants-list")
        cls.path_individual_booking = reverse(
            "event-participants-detail",
            args=[cls.mentor.profile.id],
        )
        cls.path_events = reverse("events")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def url_returns_405_not_allowed_test_utility(
        self, client, url, method_names
    ):
        """Helper. Tests "url" for not allowed methods.

        It translates "methods_names" to correspond methods on "client" and
        asserts when error different from 405 (not allowed) returns.
        """

        for method_name in method_names:
            with self.subTest(method_name):
                method = getattr(client, method_name)
                response = method(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                    msg=(
                        f"Убедитесь, что для '{url}' "
                        f"метод '{method_name}' запрещен и возвращает "
                        f"правильный номер ошибки."
                    ),
                )

    def url_returns_404_not_found_test_utility(
        self, client, url, method_names
    ):
        """Helper. Tests "url" for 404 with provided methods.

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
                        f"Убедитесь, для индивидуальных URL, таких как"
                        f"'{url}' при запросе методом '{method_name}'"
                        f"возвращается ошибка 404"
                    ),
                )

    def test_events_unauthorized_client(self):
        """Unauthorized client gets 401 error on 'events' url."""
        client = AfishaURLTests.unauthorized_client
        response = client.get(AfishaURLTests.path_events)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=(
                f"Проверьте что неавторизованный пользователь не имеет "
                f"доступ к '{AfishaURLTests.path_events}'."
            ),
        )

    def test_events_participants_unauthorized_client(self):
        """Unauthorized client gets 401 error on 'event-participants' url."""
        client = AfishaURLTests.unauthorized_client
        response = client.get(AfishaURLTests.path_events_participants)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=(
                f"Проверьте что неавторизованный пользователь не имеет доступ "
                f"к '{AfishaURLTests.path_events_participants}'."
            ),
        )

    def test_events_mentor_has_access(self):
        """Mentor gets response with 200 code on 'events'."""
        user = AfishaURLTests.mentor
        client = self.return_authorized_user_client(user=user)
        response = client.get(AfishaURLTests.path_events)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=(
                f"Проверьте что пользователь с ролью "
                f"'{user.profile.role}' "
                f"имеет доступ к "
                f"'{AfishaURLTests.path_events_participants}'."
            ),
        )

    def test_event_participants_mentor_has_access(self):
        """Mentor gets response with 200 code on 'events_participants'."""
        user = AfishaURLTests.mentor
        client = self.return_authorized_user_client(user=user)
        response = client.get(AfishaURLTests.path_events_participants)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=(
                f"Проверьте что пользователь с ролью "
                f"'{user.profile.role}' "
                f"имеет доступ к "
                f"'{AfishaURLTests.path_events_participants}'."
            ),
        )

    def test_events_individual_urls_return_404(self):
        """URLs like '/events/{id}' should return 404 for tested methods."""
        methods_to_test = [
            "get",
            "patch",
            "post",
            "put",
            "delete",
        ]
        event_id = AfishaURLTests.event.id
        individual_event_url = AfishaURLTests.path_events + str(event_id)

        client = self.return_authorized_user_client(AfishaURLTests.mentor)

        self.url_returns_404_not_found_test_utility(
            client=client,
            url=individual_event_url,
            method_names=methods_to_test,
        )

    def test_events_participants_individual_urls_return_405(self):
        """URLs like '/events-participants/{id}' should return 405.

        HTTP_405_METHOD_NOT_ALLOWED should be returned only for methods in
        'not_allowed_method_names' list.
        """

        not_allowed_method_names = [
            "get",
            "patch",
            "post",
            "put",
        ]
        individual_booking_url = AfishaURLTests.path_individual_booking
        client = self.return_authorized_user_client(AfishaURLTests.mentor)

        self.url_returns_405_not_allowed_test_utility(
            client=client,
            url=individual_booking_url,
            method_names=not_allowed_method_names,
        )

    def test_events_list_url_returns_405(self):
        """URL '/events/' should return 405.

        HTTP_405_METHOD_NOT_ALLOWED should be returned only for methods in
        'not_allowed_method_names' list.
        """

        not_allowed_method_names = [
            "patch",
            "post",
            "put",
            "delete",
        ]
        events_url = AfishaURLTests.path_events

        client = self.return_authorized_user_client(AfishaURLTests.mentor)

        self.url_returns_405_not_allowed_test_utility(
            client=client,
            url=events_url,
            method_names=not_allowed_method_names,
        )

    def test_events_participants_list_returns_405(self):
        """URL '/events_participants/' should return 405.

        HTTP_405_METHOD_NOT_ALLOWED should be returned only for methods in
        'not_allowed_method_names' list.
        """

        not_allowed_method_names = [
            "patch",
            "put",
            "delete",
        ]
        events_participants_url = AfishaURLTests.path_events_participants

        client = self.return_authorized_user_client(AfishaURLTests.mentor)

        self.url_returns_405_not_allowed_test_utility(
            client=client,
            url=events_participants_url,
            method_names=not_allowed_method_names,
        )
