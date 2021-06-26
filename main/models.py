from django.db import models

from places.models import Place
from questions.models import Question


class Main(models.Model):
    place = models.OneToOneField(
        Place, on_delete=models.RESTRICT, verbose_name="Место - куда пойти?"
    )
    questions = models.ManyToManyField(Question, verbose_name="Вопросы")
    # history = models.OneToOneField(History, on_delete=models.RESTRICT)
    # articles = models.ManyToManyField(Article, )
    # movies = models.ManyToManyField(Movie,)
    # video = models.OneToOneField(Video, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    def __str__(self):
        return "Редактировать"


TEMP_DATA = {
    "history": {
        "id": 21,
        "imageUrl": "https://picsum.photos/870/520",
        "title": "История Марины и Алины",
    },
    "articles": [
        {
            "id": 41,
            "color": "#C8D1FF",
            "title": (
                "Развитие детей-сирот отличается от развития детей, "
                "живущих в семьях. Все  этапы развития у детей-сирот "
                "проходят с искажениями и имеют ряд негативных "
                "особенностей. "
            ),
        },
        {
            "id": 42,
            "color": "#8CDD94",
            "title": (
                "У таких детей возникает ощущение отверженности. Оно "
                "приводит к напряженности и  недоверию к людям и, как "
                "итог, к реальному неприятию себя и окружающих."
            ),
        },
    ],
    "movies": [
        {
            "id": 51,
            "imageUrl": "https://picsum.photos/420/239",
            "title": "Жутко громко и запредельно близко",
            "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
            "link": "https://youtu.be/8VzzlhOyOSI",
            "tags": ["rubric", "rubric2"],
        },
        {
            "id": 52,
            "imageUrl": "https://picsum.photos/420/239",
            "title": "Жутко громко и запредельно близко",
            "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
            "link": "https://youtu.be/8VzzlhOyOSI",
            "tags": ["rubric", "rubric2"],
        },
        {
            "id": 53,
            "imageUrl": "https://picsum.photos/420/239",
            "title": "Жутко громко и запредельно близко",
            "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
            "link": "https://youtu.be/8VzzlhOyOSI",
            "tags": ["rubric", "rubric2"],
        },
        {
            "id": 54,
            "imageUrl": "https://picsum.photos/420/239",
            "title": "Жутко громко и запредельно близко",
            "info": "Василий Сигарев, Борисов-Мусотов (Россия), 2009 год",
            "link": "https://youtu.be/8VzzlhOyOSI",
            "tags": ["rubric", "rubric2"],
        },
    ],
    "video": {
        "id": 61,
        "title": "Эфир с выпускником нашей программы",
        "info": "Иван Рустаев, выпускник программы",
        "link": "https://youtu.be/H980rXfjdq4",
        "imageUrl": "https://picsum.photos/1199/675",
        "duration": 134,
    },
}
