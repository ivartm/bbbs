from django.db import models

from bbbs.entertainment.models import Article, Movie, Video
from bbbs.places.models import Place
from bbbs.questions.models import Question
from bbbs.story.models import Story


class Main(models.Model):
    place = models.OneToOneField(
        Place, on_delete=models.RESTRICT, verbose_name="Место - куда пойти?"
    )
    questions = models.ManyToManyField(Question, verbose_name="Вопросы")
    history = models.OneToOneField(
        Story,
        null=True,
        blank=False,
        on_delete=models.RESTRICT,
        verbose_name="История",
    )
    articles = models.ManyToManyField(Article, verbose_name="Статьи")
    movies = models.ManyToManyField(Movie, verbose_name="Фильмы")
    video = models.OneToOneField(
        Video,
        null=True,
        blank=False,
        on_delete=models.RESTRICT,
        verbose_name="Видео",
    )

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    def __str__(self):
        return "Редактировать"
