import random

import factory
from faker import Faker

from entertainment.models import Article, Book, BookTag, Guide

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


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
        django_get_or_create = ["title"]

    title = factory.Sequence(lambda n: fake.unique.sentence(nb_words=6))
    author = factory.Sequence(lambda n: fake.unique.name())
    profession = factory.Sequence(lambda n: fake.unique.sentence(nb_words=3))
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
    color = factory.Faker("color_name", locale="en_US")


class BookTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookTag
        django_get_or_create = [
            "name",
        ]

    name = factory.Faker("word")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
        django_get_or_create = ["title"]

    title = factory.Sequence(lambda n: fake.unique.sentence(nb_words=4))
    author = factory.Sequence(lambda n: fake.unique.name())
    year = factory.LazyFunction(lambda: random.randint(1900, 2021))
    description = factory.Faker("text")
    color = factory.Faker("color_name", locale="en_US")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            tags = extracted
            self.tags.add(*tags)
            return

        at_least = 1
        num = kwargs.get("num", None)
        how_many = num or at_least

        tags_count = BookTag.objects.count()
        how_many = min(tags_count, how_many)

        tags = BookTag.objects.order_by("?")[:how_many]
        self.tags.add(*tags)
