import random

import factory
from faker import Faker

from rights.models import Right, RightTag

fake = Faker(["ru_RU"])


class RightTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RightTag
        django_get_or_create = [
            "name",
        ]

    name = factory.Faker("word")


class RightFactory(factory.django.DjangoModelFactory):
    """Creates Right object with at least 1 RightTag related object.

    Requirements:
        - it doesn't create related RightTag objects but rely on them. Be sure
        they are created before use

    Keyword arguments:

        - "tags__num" if passed creates object with amount of "num_tags" tags.
        But not more than tags in db. The factory assumes that RightTag table
        is small otherwise it could take enormous time to order_by("?").

        - "tags" expects list of RightTags objects and pass it to
        object during creation.

    Examples:
        ========================
        RightFactory(tags__num=2)
        =========================
        Creates Right obj with 2 random tags (if there are 2 or more tags
        in DB).

        =========================
        tag_1 = RightTagFactory(...)
        tag_2 = RightTagFactory(...)
        tags = [tag_1, tag_2]
        RightFactory(tags=*tags)
        =========================
        Creates Right obj with exact tag1 and tag2
    """

    class Meta:
        model = Right
        django_get_or_create = [
            "title",
        ]

    title = factory.Sequence(lambda t: f"{fake.word()} {t}")
    description = factory.Faker(
        "sentence", nb_words=10, variable_nb_words=True
    )
    with open("common/management/rights.html", "r") as text:
        text = text.read()
    image_url = factory.django.ImageField(
        color=factory.Faker("color_name", locale="en_US")
    )
    color = factory.LazyFunction(
        lambda: random.choice(Right.Colors.choices)[0]
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

        tags_count = RightTag.objects.count()
        how_many = min(tags_count, how_many)

        tags = RightTag.objects.order_by("?")[:how_many]
        self.tags.add(*tags)
