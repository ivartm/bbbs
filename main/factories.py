import factory
from faker import Faker

from entertainment.models import Article, Video, Movie
from main.models import Main
from places.models import Place

# from story.models import Story
from questions.models import Question

fake = Faker(["ru_RU"])


class MainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Main

    place = factory.Iterator(Place.objects.all())
    # history = factory.Iterator(Story.objects.all())
    video = factory.Iterator(Video.objects.all())

    @factory.post_generation
    def questions(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            questions = extracted
            self.questions.add(*questions)
            return

        at_least = 3
        questions = Question.objects.order_by("?")[:at_least]
        self.questions.add(*questions)

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            articles = extracted
            self.articles.add(*articles)
            return

        at_least = 2
        articles = Article.objects.order_by("?")[:at_least]
        self.articles.add(*articles)

    @factory.post_generation
    def movies(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            movies = extracted
            self.movies.add(*movies)
            return

        at_least = 4
        movies = Movie.objects.order_by("?")[:at_least]
        self.movies.add(*movies)
