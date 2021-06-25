import random

import factory
from django.core.management.base import BaseCommand

from afisha.factories import EventFactory
from common.factories import CityFactory
from common.models import City
from places.factories import PlaceFactory, PlacesTagFactory
from questions.factories import (
    QuestionFactory,
    QuestionFactoryWithoutAnswer,
    QuestionTagFactory,
)
from rights.factories import RightFactory, RightTagFactory
from users.factories import UserFactory

CITIES = [
    "Волгоград",
    "Астрахань",
    "Казань",
    "Железногорск",
    "Чебоксары",
    "Санкт-Петербург",
    "Москва",
]


class AllFactories:
    def create_city(self, arg):
        CityFactory.create_batch(arg)

    def create_event(self, arg):
        EventFactory.create_batch(arg)

    def create_righttag(self, arg):
        RightTagFactory.create_batch(arg)

    def create_right(self, arg):
        for _ in range(arg):
            num_tags = random.randint(1, 5)
            RightFactory(tags__num=num_tags)

    def create_user(self, arg):
        for _ in range(arg):
            num_events = random.randint(0, 5)
            UserFactory(num_events=num_events)

    def create_questiontag(self, arg):
        QuestionTagFactory.create_batch(arg)

    def create_questionwithtag(self, arg):
        for _ in range(arg):
            num_tags = random.randint(1, 15)
            QuestionFactory.create(tags=num_tags)

    def create_questionnotag(self, arg):
        QuestionFactory.create_batch(arg)

    def create_questionnoanswer(self, arg):
        QuestionFactoryWithoutAnswer.create_batch(arg)

    def create_placetag(self, arg):
        PlacesTagFactory.create_batch(arg)

    def create_place(self, arg):
        for _ in range(arg):
            num_tags = random.randint(1, 5)
            PlaceFactory.create(num_tags=num_tags)


allfactories = AllFactories()

OPTIONS_AND_FINCTIONS = {
    "city": allfactories.create_city,
    "event": allfactories.create_event,
    "righttag": allfactories.create_righttag,
    "right": allfactories.create_right,
    "user": allfactories.create_user,
    "questiontag": allfactories.create_questiontag,
    "questionwithtag": allfactories.create_questionwithtag,
    "questionnotag": allfactories.create_questionnotag,
    "questionnoanswer": allfactories.create_questionnoanswer,
    "placetag": allfactories.create_placetag,
    "place": allfactories.create_place,
}


class MyException(Exception):
    pass


class Command(BaseCommand):
    help = "Fill Data Base with test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--city",
            nargs=1,
            type=int,
            help="Creates City objects",
            required=False,
        )
        parser.add_argument(
            "--event",
            nargs=1,
            type=int,
            help="Creates Event objects",
            required=False,
        )
        parser.add_argument(
            "--righttag",
            nargs=1,
            type=int,
            help="Creates RightTag objects",
            required=False,
        )
        parser.add_argument(
            "--right",
            nargs=1,
            type=int,
            help=(
                "Creates Right object with at least 1 RightTag related object"
            ),
            required=False,
        )
        parser.add_argument(
            "--user",
            nargs=1,
            type=int,
            help="Creates User objects",
            required=False,
        )
        parser.add_argument(
            "--questiontag",
            nargs=1,
            type=int,
            help="Creates QuestionTag objects",
            required=False,
        )
        parser.add_argument(
            "--questionwithtag",
            nargs=1,
            type=int,
            help=(
                "Creates Question objects with at "
                "least 1 QuestionTag related object"
            ),
            required=False,
        )
        parser.add_argument(
            "--questionnotag",
            nargs=1,
            type=int,
            help="Creates Question objects without QuestionTag",
            required=False,
        )
        parser.add_argument(
            "--questionnoanswer",
            nargs=1,
            type=int,
            help="Creates Question objects without answers",
            required=False,
        )
        parser.add_argument(
            "--placetag",
            nargs=1,
            type=int,
            help="Creates PlaceTag objects",
            required=False,
        )
        parser.add_argument(
            "--place",
            nargs=1,
            type=int,
            help=(
                "Creates Place object with at least 1 PlaceTag related object"
            ),
            required=False,
        )

    def handle(self, *args, **options):  # noqa

        optional_arguments = 0

        for item in list(OPTIONS_AND_FINCTIONS):
            if options[item]:
                optional_arguments += 1
                with factory.Faker.override_default_locale("ru_RU"):
                    OPTIONS_AND_FINCTIONS[item](options[item][0])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{options[item][0]} {item} created successfully"
                        )
                    )

        if optional_arguments == 0:
            try:
                if City.objects.count() > len(CITIES):
                    raise MyException()

                with factory.Faker.override_default_locale("ru_RU"):
                    for city_name in CITIES:
                        CityFactory(name=city_name)

                    CityFactory.create_batch(10)

                    EventFactory.create_batch(200)

                    RightTagFactory.create_batch(10)

                    for _ in range(20):
                        num_tags = random.randint(1, 5)
                        RightFactory(tags__num=num_tags)

                    for _ in range(30):
                        num_events = random.randint(0, 5)
                        UserFactory(num_events=num_events)

                    QuestionTagFactory.create_batch(15)

                    for _ in range(30):
                        num_tags = random.randint(1, 5)
                        QuestionFactory.create(tags=num_tags)

                    QuestionFactory.create_batch(5)

                    QuestionFactoryWithoutAnswer.create_batch(5)

                    PlacesTagFactory.create_batch(15)

                    for _ in range(30):
                        num_tags = random.randint(1, 5)
                        PlaceFactory.create(num_tags=num_tags)

                self.stdout.write(
                    self.style.SUCCESS("The database is filled with test data")
                )
            except MyException:
                self.stdout.write(
                    self.style.ERROR(
                        "The database is already filled with standard test "
                        "data. To top up individual tables, use the arguments."
                    )
                )
