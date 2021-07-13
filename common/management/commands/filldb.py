import random

import factory
from django.core.management.base import BaseCommand

from afisha.factories import EventFactory
from common.factories import CityFactory, MeetingFactory
from common.management.urls_links import link_movie_list, link_video_list
from common.models import City
from entertainment.factories import (
    ArticleFactory,
    BookFactory,
    BookTagFactory,
    GuideFactory,
    MovieFactory,
    MovieTagFactory,
    VideoFactory,
    VideoTagFactory,
)
from main.factories import MainFactory
from places.factories import PlaceFactory, PlacesTagFactory
from questions.factories import (
    QuestionFactory,
    QuestionFactoryWithoutAnswer,
    QuestionTagFactory,
)
from rights.factories import RightFactory, RightTagFactory
from story.factories import StoryFactory, StoryImageFactory
from users.factories import CuratorFactory, UserFactory

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

    def create_curator(self, arg):
        for _ in range(arg):
            CuratorFactory.create_batch(arg)

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
            PlaceFactory.create(tags__num=num_tags)

    def create_guide(self, arg):
        GuideFactory.create_batch(arg)

    def create_movietag(self, arg):
        MovieTagFactory.create_batch(arg)

    def create_movie(self, arg):
        for _ in range(arg):
            num_tags = random.randint(1, 5)
            MovieFactory.create(tags__num=num_tags)

    def create_meeting(self, arg):
        MeetingFactory.create_batch(arg)

    def create_article(self, arg):
        ArticleFactory.create_batch(arg)

    def create_booktag(self, arg):
        BookTagFactory.create_batch(arg)

    def create_book(self, arg):
        BookFactory.create_batch(arg)

    def create_videotag(self, arg):
        VideoTagFactory.create_batch(arg)

    def create_history(self, arg):
        for _ in range(arg):
            StoryFactory.create()

    def create_history_image(self, arg):
        StoryImageFactory.create_batch(arg)


allfactories = AllFactories()

OPTIONS_AND_FINCTIONS = {
    "city": allfactories.create_city,
    "event": allfactories.create_event,
    "righttag": allfactories.create_righttag,
    "right": allfactories.create_right,
    "curator": allfactories.create_curator,
    "user": allfactories.create_user,
    "questiontag": allfactories.create_questiontag,
    "questionwithtag": allfactories.create_questionwithtag,
    "questionnotag": allfactories.create_questionnotag,
    "questionnoanswer": allfactories.create_questionnoanswer,
    "placetag": allfactories.create_placetag,
    "place": allfactories.create_place,
    "guide": allfactories.create_guide,
    "movietag": allfactories.create_movietag,
    "movie": allfactories.create_movie,
    "meeting": allfactories.create_meeting,
    "article": allfactories.create_article,
    "booktag": allfactories.create_booktag,
    "book": allfactories.create_book,
    "videotag": allfactories.create_videotag,
    "history": allfactories.create_history,
    "historyimg": allfactories.create_history_image,
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
            "--curator",
            nargs=1,
            type=int,
            help="Creates Curator objects",
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
        parser.add_argument(
            "--guide",
            nargs=1,
            type=int,
            help=("Creates Guide objects"),
            required=False,
        )
        parser.add_argument(
            "--movietag",
            nargs=1,
            type=int,
            help="Creates MovieTag objects",
            required=False,
        )
        parser.add_argument(
            "--movie",
            nargs=1,
            type=int,
            help=("Creates Movie object with at least 1 MovieTag object"),
            required=False,
        ),
        parser.add_argument(
            "--meeting",
            nargs=1,
            type=int,
            help="Creates Meeting objects",
            required=False,
        )
        parser.add_argument(
            "--article",
            nargs=1,
            type=int,
            help="Creates Article objects",
            required=False,
        )
        parser.add_argument(
            "--booktag",
            nargs=1,
            type=int,
            help="Creates BookTag objects",
            required=False,
        )
        parser.add_argument(
            "--book",
            nargs=1,
            type=int,
            help="Creates Book object with at least 1 BookTag related object",
            required=False,
        )
        parser.add_argument(
            "--videotag",
            nargs=1,
            type=int,
            help="Creates VideoTag objects",
            required=False,
        )
        parser.add_argument(
            "--history",
            nargs=1,
            type=int,
            help="Create Story object",
            required=False,
        )
        parser.add_argument(
            "--historyimg",
            nargs=1,
            type=int,
            help="Create StoryImage object",
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

                    CuratorFactory.create_batch(15)

                    RightTagFactory.create_batch(10)

                    for _ in range(70):
                        num_tags = random.randint(1, 5)
                        RightFactory(tags__num=num_tags)

                    for _ in range(70):
                        num_events = random.randint(0, 5)
                        UserFactory(num_events=num_events)

                    QuestionTagFactory.create_batch(15)

                    for _ in range(70):
                        num_tags = random.randint(1, 5)
                        QuestionFactory.create(tags=num_tags)

                    QuestionFactory.create_batch(5)

                    QuestionFactoryWithoutAnswer.create_batch(5)

                    PlacesTagFactory.create_batch(15)

                    for _ in range(70):
                        num_tags = random.randint(1, 5)
                        PlaceFactory.create(tags__num=num_tags)

                    GuideFactory.create_batch(70)

                    MovieTagFactory.create_batch(15)

                    for link in link_movie_list:
                        num_tags = random.randint(1, 5)
                        MovieFactory.create(link=link, tags__num=num_tags)

                    MeetingFactory.create_batch(50)

                    ArticleFactory.create_batch(70)

                    BookTagFactory.create(
                        name="Художественные",
                        slug="hudozhestvennye",
                        color="#C8D1FF",
                    )
                    BookTagFactory.create(
                        name="Научные", slug="nauchnye", color="#FC8585"
                    )
                    BookFactory.create_batch(50)

                    VideoTagFactory.create_batch(15)

                    for link in link_video_list:
                        num_tags = random.randint(1, 5)
                        VideoFactory.create(link=link, tags__num=num_tags)

                    for _ in range(30):
                        StoryFactory.create()

                    StoryImageFactory.create_batch(100)

                    MainFactory.create()

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
