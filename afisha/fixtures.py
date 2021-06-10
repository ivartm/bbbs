import factory

from afisha.factories import EventParticipantFactory
from common.factories import CityFactory
from questions.factories import TagFactory, QuestionFactory

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
    """Create City, User, Profile, Event, EventParticipant fixtures."""
    with factory.Faker.override_default_locale("ru_RU"):
        for city_name in CITIES:
            CityFactory(name=city_name)
            EventParticipantFactory.create_batch(200)
            TagFactory.create_batch(15)        
            QuestionFactory.create_batch(50)
