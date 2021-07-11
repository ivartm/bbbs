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

    @factory.lazy_attribute
    def title(self):
        first_friend = fake.first_name()
        second_friend = fake.first_name()
        title = first_friend + " и " + second_friend
        trunc_title = title[:28] + ".." if len(title) > 30 else title

        return trunc_title
