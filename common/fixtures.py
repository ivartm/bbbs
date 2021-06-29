import random

import factory

from afisha.factories import EventFactory
from common.factories import CityFactory
from places.factories import PlaceFactory, PlacesTagFactory
from questions.factories import (
    QuestionFactory,
    QuestionFactoryWithoutAnswer,
    QuestionTagFactory,
)
from rights.factories import RightFactory, RightTagFactory
from users.factories import UserFactory

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

        CityFactory.create_batch(10)
        EventFactory.create_batch(200)

        RightTagFactory.create_batch(10)
        for _ in range(20):
            amount = random.randint(1, 5)
            RightFactory(tags__num=amount)

        for _ in range(30):
            amount = random.randint(0, 5)
            UserFactory.create(num_events=amount)

        QuestionTagFactory.create_batch(15)
        # make Questions with tags
        for _ in range(30):
            amount = random.randint(1, 15)
            QuestionFactory.create(tags=amount)

        # make Questions without tags
        QuestionFactory.create_batch(5)
        # make Questions without tags and answers
        QuestionFactoryWithoutAnswer.create_batch(5)

        PlacesTagFactory.create_batch(15)

        for _ in range(30):
            amount = random.randint(1, 15)
            PlaceFactory.create(tags__num=amount)


if __name__ == "__main__":
    make_fixtures()
