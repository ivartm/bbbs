import random
from django.contrib.auth import get_user_model

import factory

from afisha.factories import EventFactory
from common.factories import CityFactory
from questions.factories import (
    QuestionFactory,
    QuestionFactoryWithoutAnswer,
    QuestionTagFactory,
)
from rights.factories import RightFactory, RightTagFactory
from users.factories import UserFactory


User = get_user_model()


CITIES = [
    "Волгоград",
    "Астрахань",
    "Казань",
    "Железногорск",
    "Чебоксары",
    "Санкт-Петербург",
    "Москва",
]

ADMIN_USERNAME = "bbbs"
ADMIN_PASSWORD = "Bbbs2021!"
ADMIN_EMAIL = "admin@bbbs.ru"


def make_fixtures():
    """Fixtures for the models

    City, User, Profile, Event, EventParticipant, QuestionTag, Question
    """

    User.objects.create_superuser(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD,
    )

    with factory.Faker.override_default_locale("ru_RU"):
        for city_name in CITIES:
            CityFactory(name=city_name)

        CityFactory.create_batch(10)
        EventFactory.create_batch(200)

        RightTagFactory.create_batch(10)
        for _ in range(20):
            num_tags = random.randint(1, 5)
            RightFactory(num_tags=num_tags)

        for _ in range(30):
            num_events = random.randint(0, 5)
            UserFactory(num_events=num_events)

        QuestionTagFactory.create_batch(15)
        # make Questions with tags
        for _ in range(30):
            num_tags = random.randint(1, 15)
            QuestionFactory.create(tags=num_tags)
        # make Questions without tags
        QuestionFactory.create_batch(5)
        # make Questions without tags and answers
        QuestionFactoryWithoutAnswer.create_batch(5)
