import factory
from faker import Faker

from rights.models import Right, RightTag

fake = Faker(["ru_RU"])


class RightTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RightTag
        django_get_or_create = ["name"]

    name = factory.Faker("word")


class RightFactory(factory.django.DjangoModelFactory):
    """Creates Right object with at least 1 RightTag related object.

    Requirements:
        - it doesn't create related RightTag objects but rely on them. Be sure
        they are created before use

    Keyword arguments:
        - "num_tags" if passed creates object with amount of "num_tags" tags.
        But not more than tags in db.

    The factory assumes that RightTag table is small otherwise it could take
    enormous time to order_by("?")

    """

    class Meta:
        model = Right

    title = factory.Sequence(lambda t: f"{fake.word()} {t}")
    description = factory.Faker("sentence", nb_words=6, variable_nb_words=True)
    text = factory.Faker(
        "paragraph",
        nb_sentences=3,
        variable_nb_sentences=True,
    )
    color = factory.Faker("color_name", locale="en_US")
    imageUrl = factory.django.ImageField(
        color=factory.Faker("color_name", locale="en_US")
    )

    @factory.post_generation
    def num_tags(self, create, extracted, **kwargs):
        if not create:
            return

        at_least = 1
        how_many = extracted or at_least

        tags_count = RightTag.objects.count()
        how_many = min(tags_count, how_many)

        tags = RightTag.objects.order_by("?")[:how_many]
        self.tag.add(*tags)
