from rights.factories import RightFactory, RightTagFactory
import factory
import random

# from afisha.factories import EventParticipantFactory
from common.factories import CityFactory

# from questions.factories import QuestionTagFactory, QuestionFactory

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

        # EventParticipantFactory.create_batch(20)
        # QuestionTagFactory.create_batch(15)
        # QuestionFactory.create_batch(50)

        RightTagFactory.create_batch(50)
        for _ in range(50):
            num_tags = random.randint(1, 10)
            RightFactory(num_tags=num_tags)
