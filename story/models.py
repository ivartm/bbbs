from django.db import models


class Story(models.Model):
    image_url = models.ImageField(
        upload_to="stories/",
        verbose_name="Фото",
        help_text="Загрузите фото",
        blank=True,
    )
    title = models.CharField(
        verbose_name="Название истории", max_length=30, unique=True
    )
    beginning_of_friendship = models.DateField(
        verbose_name="Дата начала дружбы"
    )
    prolog = models.TextField(verbose_name="Пролог")
    text = models.TextField(verbose_name="Текст истории")
    passage = models.TextField(verbose_name="Цитата из текста")
    pub_date = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )

    class Meta:
        ordering = ("-beginning_of_friendship",)
        verbose_name = "История"
        verbose_name_plural = "Истории"

    def __str__(self):
        return self.title


class StoryImage(models.Model):
    story = models.ForeignKey(
        Story,
        related_name="stories",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name="Фотография", upload_to="stories/", blank=True
    )
