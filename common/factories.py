import random

import factory
from django.contrib.auth import get_user_model
from faker import Faker

from common.models import City, Meeting
from users.models import Profile

User = get_user_model()

fake = Faker(["ru-RU"])


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = [
            "name",
        ]

    name = factory.Faker("city")
    isPrimary = factory.Faker(
        "boolean",
        chance_of_getting_true=20,
    )


class MeetingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meeting

    user = factory.Iterator(
        User.objects.filter(profile__role=Profile.Role.MENTOR)
    )
    image = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )
    description = factory.Faker("text")
    smile = factory.LazyFunction(
        lambda: random.choice([Meeting.GLAD, Meeting.SAD, Meeting.NORMAL])
    )
    place = factory.Faker("text")
    date = factory.Faker(
        "date",
    )
    send_to_curator = factory.LazyFunction(
        lambda: random.choice([False, True])
    )
