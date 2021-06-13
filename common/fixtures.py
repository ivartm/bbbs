import random

import factory

from afisha.factories import EventParticipantFactory
from common.factories import CityFactory
from questions.factories import (
    QuestionFactory,
    QuestionFactoryWithoutAnswer,
    TagFactory,
)
from questions.models import QuestionTag
from rights.factories import RightFactory, RightTagFactory

CITIES = [
    "Волгоград",
    "Астрахань",
    "Казань",
    "Железногорск",
    "Чебоксары",
    "Санкт-Петербург",
    "Москва",
]


def make_fixtures():
    """Fixtures for the models

    City, User, Profile, Event, EventParticipant, QuestionTag, Question
    """
    with factory.Faker.override_default_locale("ru_RU"):
        for city_name in CITIES:
            CityFactory(name=city_name)

        TagFactory.create_batch(15)
        EventParticipantFactory.create_batch(200)
        # make Questions with tags
        tag_list = list(QuestionTag.objects.all())
        for _ in range(30):
            random_tag = random.randint(0, 14)
            QuestionFactory.create(tags=[tag_list[random_tag]])
        # make Questions without tags
        QuestionFactory.create_batch(5)
        # make Questions without tags and answers
        QuestionFactoryWithoutAnswer.create_batch(5)

        RightTagFactory.create_batch(50)
        for _ in range(50):
            num_tags = random.randint(1, 10)
            RightFactory(num_tags=num_tags)
