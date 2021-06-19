import json
from datetime import datetime

import pytz
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from common.factories import CityFactory
from users.factories import UserFactory

from afisha.factories import EventFactory, EventParticipantFactory
from afisha.models import EventParticipant


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

    def test_response_is_paginated(self):
        """Just look for 'next', 'previous', 'result' keys in response."""
        user = ViewAfishaTests.mentor
        EventFactory.create_batch(50, city=user.profile.city)
        client = self.return_authorized_user_client(user)

        response_data = client.get(
            path=self.path_events,
        ).data

        self.assertTrue("next" in response_data)
        self.assertTrue("previous" in response_data)
        self.assertTrue("results" in response_data)

    def test_mentor_can_list_available_events_in_his_city(self):
        """Looks for amount recodes in response.

        The test assumes that pages size is less or equal 10.
        """

        city = CityFactory(name="Вермонт")
        other_city = ViewAfishaTests.city
        user = UserFactory(profile__city=city)
        client = self.return_authorized_user_client(user)
        EventFactory.create_batch(10, city=city)
        EventFactory.create_batch(100, city=other_city)

        response = client.get(
            path=self.path_events,
        )
        results = response.data.get("results")

        self.assertEqual(
            len(results),
            10,
            msg=(
                "Проверьте что пользователь видит все доступные события "
                "в городе"
            ),
        )

    def test_mentor_can_book_event(self):
        """Looks for status code and returned JSON in response"""
        user = ViewAfishaTests.mentor
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

        self.assertEqual(
            response.status_code,
            201,
            msg=(
                "Проверьте, что при успешной регистрации "
                "возвращается статус 201."
            ),
        )

        event_participate_record = EventParticipant.objects.get(
            user=user, event=event
        )
        expected_data = {
            "id": event_participate_record.id,
            "event": event.id,
        }
        self.assertEqual(
            response.data,
            expected_data,
            msg=("Проверьте, что возвращается правильный JSON."),
        )

    def test_booked_event_has_true_flag(self):
        """Looks fot "booked" string in response record."""
        user = ViewAfishaTests.mentor
        event = EventFactory.create(city=user.profile.city)
        EventParticipantFactory.create(
            event=event,
            user=user,
        )

        client = self.return_authorized_user_client(user)
        response_data = client.get(
            path=ViewAfishaTests.path_events,
            format="json",
        ).data

        results = response_data.get("results")
        record_dict = results[0]

        self.assertEqual(
            "True",
            str(record_dict.get("booked")),
            msg=(
                "Проверьте, что у мероприятий на которые "
                "пользователь подписан возвращается флаг "
                "booked': True."
            ),
        )

    def test_mentor_cant_book_event_with_empty_seats(self):
        user = ViewAfishaTests.mentor
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

    def test_mentor_cant_book_event_in_past(self):
        user = ViewAfishaTests.mentor
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

    def test_mentor_cant_book_same_event_twice(self):
        user = ViewAfishaTests.mentor
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

    def test_mentor_cant_book_event_in_other_city(self):
        user = ViewAfishaTests.mentor
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

    def test_mentor_can_unbook_event(self):
        user = ViewAfishaTests.mentor
        event = EventFactory.create(
            city=user.profile.city,
        )
        EventParticipantFactory.create(
            user=user,
            event=event,
        )
        path = reverse("event-participants-detail", args=[event.id])

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
            ),
        )

        self.assertEqual(
            response.status_code,
            204,
            msg=(
                "Проверьте, что при удачной отписке от мероприятия "
                "возвращается код 204"
            ),
        )

    def test_mentor_sees_events_in_the_his_own_city_only(self):
        """Looks for amount records in responses for different users.

        user = don't have any records in his city. We expect zero records.
        users_other_city = has to have 10 records.

        The test assumes that page size is more than 10 records.
        """

        other_city = CityFactory.create()
        user = ViewAfishaTests.mentor
        user_other_city = UserFactory.create(profile__city=other_city)
        EventFactory.create_batch(10, city=other_city)

        client_user = self.return_authorized_user_client(user)
        response_data = client_user.get(
            ViewAfishaTests.path_events, format="json"
        ).data
        dict_expected_len_zero = response_data.get("results")

        self.assertEqual(
            len(dict_expected_len_zero),
            0,
            msg=(
                "Убедитесь, что пользователю не возвращаются мероприятия "
                "в других городах."
            ),
        )

        client_other_user = self.return_authorized_user_client(user_other_city)
        response_data = client_other_user.get(
            ViewAfishaTests.path_events, format="json"
        ).data
        dict_expected_len_equals_ten = response_data.get("results")

        self.assertEqual(
            len(dict_expected_len_equals_ten),
            10,
            msg=(
                "Убедитесь, что пользователю показывается мероприятие в его "
                "городе."
            ),
        )
