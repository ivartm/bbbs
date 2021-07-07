import random

import factory
from faker import Faker

from entertainment.models import Guide, Movie, MovieTag

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

class MovieTagFactory(factory.django.DjangoModelFactory):
    """This factory creates movies' tags."""

    class Meta:
        model = MovieTag

    name = factory.Sequence(lambda n: fake.unique.word())


class MovieFactory(factory.django.DjangoModelFactory):
    """This factory creates Movies."""

    class Meta:
        model = Movie
        django_get_or_create = ["title"]

    title = factory.Sequence(lambda n: fake.unique.sentence(nb_words=7))
    description = factory.Sequence(lambda n: fake.unique.sentence(nb_words=50))
    info = factory.Sequence(lambda n: fake.unique.sentence(nb_words=50))
    link = factory.Sequence(lambda n: fake.unique.sentence(nb_words=20))
    preview = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        if not created:
            return

        at_least = 1
        how_many = extracted or at_least

        tags_count = MovieTag.objects.count()
        how_many = min(tags_count, how_many)

        tags = MovieTag.objects.order_by("?")[:how_many]
        self.tags.add(*tags)