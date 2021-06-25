import random

import factory
from faker import Faker

from places.models import Place, PlaceTag

fake = Faker(["ru_RU"])


class PlacesTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaceTag
        django_get_or_create = ["name"]

    name = factory.Faker("word")


class PlaceFactory(factory.django.DjangoModelFactory):
    """
    Creates Place object with at least 1 PlaceTag related object.

    Requirements:
        - it doesn't create related PlaceTag objects but rely on them. Be sure
        they are created before use

    Keyword arguments:
        - "num_tags" if passed creates object with amount of "num_tags" tags.
        But not more than tags in db.

    The factory assumes that PlaceTag table is small otherwise it could take
    enormous time to order_by("?")
    """

    class Meta:
        model = Place

    chosen = factory.LazyFunction(lambda: random.choice([True, False]))
    title = factory.Sequence(lambda n: fake.unique.sentence(nb_words=7))
    address = factory.Faker("address")
    gender = factory.LazyFunction(
        lambda: random.choice(Place.Genders.choices)[0]
    )
    age = factory.LazyFunction(lambda: random.randint(5, 17))
    activity_type = factory.LazyFunction(
        lambda: random.choice(Place.ActivityTypes.choices)[0]
    )
    description = factory.Faker("text")
    imageUrl = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )
    link = factory.Sequence(lambda n: fake.unique.domain_name())

    @factory.post_generation
    def num_tags(self, create, extracted, **kwargs):
        if not create:
            return

        at_least = 1
        how_many = extracted or at_least

        tags_count = PlaceTag.objects.count()
        how_many = min(tags_count, how_many)

        tags = PlaceTag.objects.order_by("?")[:how_many]
        self.tags.add(*tags)
