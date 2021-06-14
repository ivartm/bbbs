import factory
import pytz
from faker import Faker

from questions.models import Question, QuestionTag

fake = Faker(["ru-RU"])


class QuestionTagFactory(factory.django.DjangoModelFactory):
    """Create Tag objects."""

    class Meta:
        model = QuestionTag

    name = factory.Sequence(lambda n: fake.unique.word())


class QuestionFactory(factory.django.DjangoModelFactory):
    """This factory creates Questions."""

    class Meta:
        model = Question

    question = factory.Sequence(lambda n: fake.unique.sentence(nb_words=7))
    answer = factory.Faker("text")
    pubDate = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=pytz.UTC,
    )

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        if not created:
            return

        at_least = 1
        how_many = extracted or at_least

        tags_count = QuestionTag.objects.count()
        how_many = min(tags_count, how_many)

        tags = QuestionTag.objects.order_by("?")[:how_many]
        self.tags.add(*tags)


class QuestionFactoryWithoutAnswer(factory.django.DjangoModelFactory):
    """This factory creates Questions without answers"""

    class Meta:
        model = Question

    question = factory.Sequence(lambda n: fake.unique.sentence(nb_words=7))
    pubDate = factory.Faker(
        "date_time_this_year",
        before_now=False,
        after_now=True,
        tzinfo=pytz.UTC,
    )
