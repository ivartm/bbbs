# from datetime import timedelta

from enum import unique
import factory
import pytz
from faker import Faker
import random

from questions.management.slug_transliteration import slugify
from questions.models import Question, Tag
# from common.models import City
# from users.factories import UserFactory

fake = Faker(["ru-RU"])


class TagFactory(factory.django.DjangoModelFactory):
    """Create Tag objects."""

    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: fake.unique.word())
    # name = factory.Faker("color_name")
    # address = factory.Faker("address")
    # contact = factory.LazyAttribute(
    #     lambda x: f"{fake.name()}, {fake.phone_number()}"
    # )
    # title = factory.Sequence(lambda t: f"{fake.sentence(nb_words=3)} {t}")
    # description = factory.Faker("text")
    # startAt = factory.Faker(
    #     "date_time_this_year",
    #     before_now=False,
    #     after_now=True,
    #     tzinfo=pytz.UTC,
    # )
    # endAt = factory.Faker(
    #     "date_time_between",
    #     start_date=factory.SelfAttribute("..startAt"),
    #     end_date=factory.LazyAttribute(
    #         lambda obj: obj.start_date + timedelta(days=60)
    #     ),
    #     tzinfo=pytz.UTC,
    # )
    # seats = factory.Faker("random_int", min=0, max=50)
    # city = factory.Iterator(City.objects.all())


class QuestionFactory(factory.django.DjangoModelFactory):
    """This factory creates Questions."""

    class Meta:
        model = Question

    tag = factory.RelatedFactory(TagFactory)
    question = factory.Sequence(lambda n: fake.unique.sentence(nb_words=7))
    answer = factory.Faker("text")
    pubDate = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=pytz.UTC,
    )
