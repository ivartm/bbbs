import datetime
import random
import urllib

import factory
from django.core.files.base import ContentFile
from faker import Faker

from story.models import Story, StoryImage

fake = Faker(["ru-RU"])


class StoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Story
        django_get_or_create = ["title"]

    prolog = factory.Faker(
        "paragraph",
        nb_sentences=15,
        variable_nb_sentences=True,
    )
    text = factory.Faker(
        "paragraph",
        nb_sentences=200,
        variable_nb_sentences=True,
    )

    @factory.lazy_attribute
    def title(self):
        first_friend = fake.first_name()
        second_friend = fake.first_name()
        title = first_friend + " и " + second_friend
        trunc_title = title[:28] + ".." if len(title) > 30 else title

        return trunc_title

    @factory.lazy_attribute
    def beginning_of_friendship(self):
        year = random.randint(2015, 2020)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = datetime.date(year, month, day)
        return date

    @factory.post_generation
    def passage(self, created, extracted, **kwargs):
        if not created:
            return

        self.passage = ".".join((self.text).split(".")[1:7])

    @factory.post_generation
    def image_url(self, created, extracted, **kwargs):
        if not created:
            return

        image = urllib.request.urlopen("https://picsum.photos/800/600").read()
        self.image_url.save(
            self.title + ".jpg", ContentFile(image), save=False
        )


class StoryImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StoryImage

    story = factory.Iterator(Story.objects.all())

    @factory.post_generation
    def image(self, created, extracted, **kwargs):
        if not created:
            return

        image = urllib.request.urlopen("https://picsum.photos/800/600").read()
        self.image.save(
            f"{self.story.title}.jpg", ContentFile(image), save=False
        )
