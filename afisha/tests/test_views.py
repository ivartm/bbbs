from datetime import datetime

import json
import pytz
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from common.factories import CityFactory
from users.factories import UserFactory

from ..factories import EventFactory, EventParticipantFactory
from ..models import EventParticipant


class ViewAfishaTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.city = CityFactory.create(name="Воркута")
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

        cls.unauthorized_client = APIClient()

        cls.path_events_participants = reverse("event-participants-list")
        cls.path_events = reverse("events")

    def return_authorized_user_client(self, user):
        authorized_client = APIClient()
        authorized_client.force_authenticate(user=user)
        return authorized_client

    def test_user_can_list_available_events_in_his_city(self):
        """Test should be rewritten to support pagination."""
        city = CityFactory(name="Вермонт")
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

    def test_allowed_user_can_book_event(self):
        for user in ViewAfishaTests.users:
            with self.subTest(user=user):
                event = EventFactory.create(
                    city=user.profile.city,
                    seats=40,
                )

                client = self.return_authorized_user_client(user)
                data = {"event": event.id}
                response = client.post(
                    path=ViewAfishaTests.path_events_participants,
                    data=data,
                    format="json",
                )
                event_participate_record = EventParticipant.objects.get(
                    user=user,
                    event=event
                )
                expected_data = {
                    "id": event_participate_record.id,
                    "event": event.id,
                }

                self.assertEqual(
                    response.status_code,
                    201,
                    msg=(
                        "Проверьте, что при успешной регистрации "
                        "возвращается статус 201."
                    ),
                )
                self.assertEqual(
                    response.data,
                    expected_data,
                    msg=(
                        "Проверьте, что возвращается правильный JSON."
                    ),
                )

    def test_booked_event_has_true_flag(self):
        """Test should be rewritten when filters become supported in API."""
        user = ViewAfishaTests.mentor
        event = EventFactory.create(
            city=user.profile.city
        )
        EventParticipantFactory.create(
            event=event,
            user=user,
        )

        client = self.return_authorized_user_client(user)
        response = client.get(
            path=ViewAfishaTests.path_events,
            format="json",
        )
        response_record_dict = response.json()[0]

        self.assertEqual(
            "True",
            str(response_record_dict.get('booked')),
            msg=(
                "Проверьте, что у мероприятий на которые "
                "пользователь подписан возвращается флаг "
                "booked': True."
            ),
        )

    def test_user_cant_book_event_with_empty_seats(self):
        for user in ViewAfishaTests.users:
            with self.subTest(user=user):
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
                    path=ViewAfishaTests.path_events_participants,
                    data=data,
                    format="json",
                )

                self.assertContains(
                    response,
                    status_code=400,
                    text="Извините, мест больше нет.",
                    msg_prefix=(
                        f"Проверьте, что пользователь с правами "
                        f"'{user.profile.role}'не может зарегистрироваться "
                        f"на мероприятие на котором закончились места."
                    ),
                )

    def test_user_cant_book_event_in_past(self):
        for user in ViewAfishaTests.users:
            with self.subTest(user=user):
                event = EventFactory.create(
                    city=user.profile.city,
                    startAt=datetime(2019, 1, 1, tzinfo=pytz.utc),
                    endAt=datetime(2020, 1, 1, tzinfo=pytz.utc),
                )

                client = self.return_authorized_user_client(user)
                data = {"event": event.id}
                response = client.post(
                    path=ViewAfishaTests.path_events_participants,
                    data=data,
                    format="json",
                )

                self.assertContains(
                    response,
                    status_code=400,
                    text="Мероприятие уже закончилось.",
                    msg_prefix=(
                        f"Проверьте, что пользователь с правами "
                        f"'{user.profile.role}'не может зарегистрироваться "
                        f"на мероприятие в прошлом."
                    ),
                )

    def test_user_cant_book_same_event_twice(self):
        for user in ViewAfishaTests.users:
            with self.subTest(user=user):
                event = EventFactory.create(
                    city=user.profile.city,
                    seats=10,
                )
                EventParticipantFactory.create(
                    user=user,
                    event=event,
                )

                client = self.return_authorized_user_client(user)
                data = {"event": event.id}
                response = client.post(
                    path=ViewAfishaTests.path_events_participants,
                    data=data,
                    format="json",
                )

                self.assertContains(
                    response,
                    status_code=400,
                    text="Вы уже зарегистрированы на это мероприятие.",
                    msg_prefix=(
                        f"Проверьте, что пользователь c ролью "
                        f"'{user.profile.role}'не может зарегистрироваться "
                        f"на мероприятие дважды. Вернулось ошибка: "
                        f"{json.loads(response.content)}"
                    ),
                )

    def test_user_cant_book_event_in_other_city(self):
        for user in ViewAfishaTests.users:
            with self.subTest(user=user):
                other_city = CityFactory()
                event = EventFactory.create(
                    city=other_city,
                )

                client = self.return_authorized_user_client(user)
                data = {"event": event.id}
                response = client.post(
                    path=ViewAfishaTests.path_events_participants,
                    data=data,
                    format="json",
                )

                self.assertContains(
                    response,
                    status_code=400,
                    text="Извините, но мероприятие не в Вашем городе.",
                    msg_prefix=(
                        f"Проверьте, что пользователь c ролью "
                        f"'{user.profile.role}'не может зарегистрироваться "
                        f"на мероприятие в другом городе."
                    ),
                )

    def test_user_can_unbook_event(self):
        for user in ViewAfishaTests.users:
            with self.subTest(user=user):
                event = EventFactory.create(
                    city=user.profile.city,
                )
                EventParticipantFactory.create(
                    user=user,
                    event=event,
                )
                path = reverse(
                    "event-participants-detail",
                    args=[event.id]
                )

                client = self.return_authorized_user_client(user)
                response = client.delete(
                    path=path,
                    format="json",
                )
                is_booked = EventParticipant.objects.filter(
                    user=user,
                    event=event,
                ).exists()

                self.assertFalse(
                    is_booked,
                    msg=(
                        f"Проверьте, что зарегистрированный пользователь "
                        f"с ролью '{user.profile.role}'"
                        f" может отписаться от мероприятия."
                    )
                )

                self.assertEqual(
                    response.status_code,
                    204,
                    msg=(
                        "Проверьте, что при удачной отписке от мероприятия "
                        "возвращается код 204"
                    ),
                )
