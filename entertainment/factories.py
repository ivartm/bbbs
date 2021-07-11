import random
from datetime import timedelta

import factory
import pytz
from faker import Faker

from entertainment.models import (
    Article,
    Book,
    BookTag,
    Guide,
    Movie,
    MovieTag,
    Video,
    VideoTag,
)

fake = Faker(["ru-RU"])


class GuideFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Guide
        django_get_or_create = ["title"]

    title = factory.Sequence(lambda n: fake.unique.sentence(nb_words=7))
    description = factory.Sequence(lambda n: fake.unique.sentence(nb_words=15))
    image_caption = factory.Sequence(
        lambda t: f"Автор фото - {fake.unique.name()}"
    )
    image_url = factory.django.ImageField(
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
    producer = factory.Sequence(lambda n: fake.unique.name())
    year = factory.LazyFunction(lambda: random.randint(1900, 2021))
    link = "https://www.youtube.com/watch?v=f0hQOVfZoIA"

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

    @factory.post_generation
    def duration(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            duration = extracted
            self.duration = duration
            return

        hours = random.randint(0, 2)
        minutes = random.randint(3, 59)
        seconds = random.randint(0, 59)

        self.duration = timedelta(
            hours=hours, minutes=minutes, seconds=seconds
        )


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
        django_get_or_create = ["title"]

    is_main = False
    title = factory.Sequence(lambda n: fake.unique.sentence(nb_words=3))
    author = factory.Sequence(lambda n: fake.unique.name())
    profession = factory.Sequence(lambda n: fake.unique.sentence(nb_words=3))
    text = factory.Faker(
        "paragraph",
        nb_sentences=3,
        variable_nb_sentences=True,
    )
    color = factory.Faker("color_name", locale="en_US")
    image_url = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )


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
    link = factory.LazyAttribute(
        lambda obj: f"http://fakebooks.bbbs/{id(obj)}-{obj.year}/"
    )

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


class VideoTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoTag
        django_get_or_create = [
            "name",
        ]

    name = factory.Faker("word")


class VideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Video
        django_get_or_create = ["title"]

    title = ""
    pub_date = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=pytz.UTC,
    )
    link = None

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

        tags_count = VideoTag.objects.count()
        how_many = min(tags_count, how_many)

        tags = VideoTag.objects.order_by("?")[:how_many]
        self.tags.add(*tags)
