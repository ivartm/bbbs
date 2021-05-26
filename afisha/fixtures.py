import factory

from .factories import (
    CityFactory,
    ProfileFactory,
    UserFactory,
    EventFactory,
    EventParticipantFactory,
)


def make_fixtures():
    with factory.Faker.override_default_locale("ru_RU"):
        CityFactory.create_batch(100)
        ProfileFactory.create_batch(100)
        UserFactory.create_batch(100)
        EventFactory.create_batch(100),
        EventParticipantFactory.create_batch(100)
