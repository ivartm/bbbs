from django.db import models

from entertainment.models import Article, Video, Movie
from places.models import Place
from questions.models import Question

from story.models import Story


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


# TEMP_DATA = {
#     "history": {
#         "id": 21,
#         "imageUrl": "https://picsum.photos/870/520",
#         "title": "История Марины и Алины",
#     },
#     "movies": [
#         {
#             "id": 51,
#             "imageUrl": "https://picsum.photos/420/239",
#             "title": "Жутко громко и запредельно близко",
#             "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
#             "link": "https://youtu.be/8VzzlhOyOSI",
#             "tags": ["rubric", "rubric2"],
#         },
#         {
#             "id": 52,
#             "imageUrl": "https://picsum.photos/420/239",
#             "title": "Жутко громко и запредельно близко",
#             "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
#             "link": "https://youtu.be/8VzzlhOyOSI",
#             "tags": ["rubric", "rubric2"],
#         },
#         {
#             "id": 53,
#             "imageUrl": "https://picsum.photos/420/239",
#             "title": "Жутко громко и запредельно близко",
#             "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
#             "link": "https://youtu.be/8VzzlhOyOSI",
#             "tags": ["rubric", "rubric2"],
#         },
#         {
#             "id": 54,
#             "imageUrl": "https://picsum.photos/420/239",
#             "title": "Жутко громко и запредельно близко",
#             "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
#             "link": "https://youtu.be/8VzzlhOyOSI",
#             "tags": ["rubric", "rubric2"],
#         },
#     ],
#     "video": {
#         "id": 61,
#         "title": "Эфир с выпускником нашей программы",
#         "info": "Иван Рустаев, выпускник программы",
#         "link": "https://youtu.be/H980rXfjdq4",
#         "imageUrl": "https://picsum.photos/1199/675",
#         "duration": 134,
#     },
# }
