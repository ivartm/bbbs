import pytz
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse

from common.factories import CityFactory
from users.factories import UserFactory
from afisha.factories import EventFactory, EventParticipantFactory

from afisha.models import EventParticipant


class ViewAfishaTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory(name="Воркута")
        cls.mentor = UserFactory(
            profile__role="mentor",
            profile__city=cls.city,
        )
        cls.moderator_reg = UserFactory(
            profile__role="moderator_reg",
            profile__city=cls.city,
        )
        cls.moderator_gen = UserFactory(
            profile__role="moderator_gen",
            profile__city=cls.city,
        )
        cls.admin = UserFactory(
            profile__role="admin",
            profile__city=cls.city,
        )
        cls.users = [
            cls.mentor,
            cls.moderator_reg,
            cls.moderator_gen,
            cls.admin,
        ]

        cls.unauthorized_client = APIClient()

        cls.path_events_participants = reverse("event-participants-list")
        cls.path_events = reverse("events")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_user_can_list_available_events_in_his_city(self):
        """Test should be rewritten to support pagination."""
        city = CityFactory(name="Вермунт")
        user = UserFactory(profile__city=city)
        client = self.return_authorized_user_client(user)
        EventFactory.create_batch(50, city=city)

        response = client.get(
            path=self.path_events,
        )

        self.assertEqual(
            len(response.data),
            50,
            msg=(
                "Проверьте что пользователь видит все доступные события "
                "в городе"
            ),
        )

    def test_allowed_user_type_can_book_event(self):
        for user in self.users:
            user = self.mentor
            event = EventFactory.create(
                city=user.profile.city,
                seats=40,
            )
            count_user_events = EventParticipant.objects.filter(
                user=user
            ).count()

            client = self.return_authorized_user_client(user)
            data = {"event": event.id}
            response = client.post(
                path=self.path_events_participants,
                data=data,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                201,
                msg=(
                    f"Проверьте, что зарегистрированный пользователь с ролью "
                    f"'{user.profile.role}' может зарегистрироваться на "
                    f"событие."
                ),
            )

            self.assertEqual(
                response.data,
                {"id": count_user_events + 1, "event": event.id},
                msg=("Проверьте, что возвращается правильный json"),
            )

    def test_user_cant_book_event_with_empty_seats(self):
        user = self.mentor
        event = EventFactory.create(
            city=user.profile.city,
            seats=40,
        )
        EventParticipantFactory.create_batch(
            40,
            event=event,
        )

        client = self.return_authorized_user_client(user)
        data = {"event": event.id}
        response = client.post(
            path=self.path_events_participants,
            data=data,
            format="json",
        )

        self.assertContains(
            response,
            status_code=400,
            text="Извините, мест больше нет.",
            msg_prefix=(
                "Проверьте, что пользователь не может зарегистрироваться "
                "на мероприятие на котором закончились места."
            ),
        )

    def test_user_cant_book_on_event_in_past(self):
        user = self.mentor
        event = EventFactory.create(
            city=user.profile.city,
            startAt=datetime(2020, 10, 27, 12, 0, 0, tzinfo=pytz.utc),
            endAt=datetime(2020, 11, 27, 12, 0, 0, tzinfo=pytz.utc),
        )

        client = self.return_authorized_user_client(user)
        data = {"event": event.id}
        response = client.post(
            path=self.path_events_participants,
            data=data,
            format="json",
        )

        self.assertContains(
            response,
            status_code=400,
            text="Мероприятие уже закончилось.",
            msg_prefix=(
                "Проверьте, что пользователь не может зарегистрироваться "
                "на мероприятие в прошлом."
            ),
        )

    def test_user_cant_book_same_event_twice(self):
        user = self.mentor
        event = EventFactory.create(
            city=user.profile.city,
        )
        EventParticipantFactory(
            user=user,
            event=event,
        )

        client = self.return_authorized_user_client(user)
        data = {"event": event.id}
        response = client.post(
            path=self.path_events_participants,
            data=data,
            format="json",
        )

        self.assertContains(
            response,
            status_code=400,
            text="Вы уже зарегистрированы на это мероприятие.",
            msg_prefix=(
                "Проверьте, что пользователь не может зарегистрироваться "
                "на мероприятие дважды."
            ),
        )

    def test_user_cant_book_event_in_other_city(self):
        user = self.mentor
        other_city = CityFactory()
        event = EventFactory.create(
            city=other_city,
        )

        client = self.return_authorized_user_client(user)
        data = {"event": event.id}
        response = client.post(
            path=self.path_events_participants,
            data=data,
            format="json",
        )

        self.assertContains(
            response,
            status_code=400,
            text="Извините, но мероприятие не в Вашем городе.",
            msg_prefix=(
                "Проверьте, что пользователь не может зарегистрироваться "
                "на мероприятие в другом городе."
            ),
        )
