import random
from datetime import date

import factory
from faker import Faker

from story.models import Story

fake = Faker(["ru-RU"])


class StoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Story
        django_get_or_create = ["title"]

    title = factory.Sequence(lambda n: fake.unique.sentence(nb_words=7))
    prolog = factory.Sequence(lambda n: fake.unique.sentence(nb_words=10))
    text = factory.Sequence(lambda n: fake.unique.sentence(nb_words=50))
    beginning_of_friendship = date.today()
    image_url = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(500, 1000)),
        height=factory.SelfAttribute("width"),
    )
