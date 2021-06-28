import random

import factory
from faker import Faker

from entertainment.models import Guide

fake = Faker(["ru-RU"])


class GuideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Guide
        django_get_or_create = ["title"]

    title = factory.Sequence(lambda n: fake.unique.sentence(nb_words=7))
    description = factory.Sequence(lambda n: fake.unique.sentence(nb_words=15))
    imageCaption = factory.Sequence(
        lambda t: f"Автор фото - {fake.unique.name()}"
    )
    imageUrl = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )
    text = factory.Faker(
        "paragraph",
        nb_sentences=3,
        variable_nb_sentences=True,
    )
