from django.db import models


class Story(models.Model):
    imageUrl = models.ImageField(
        upload_to="stories/",
        verbose_name="Фото",
        help_text="Загрузите фото",
        blank=True,
    )
    title = models.CharField(
        verbose_name="Название истории", max_length=200, unique=True
    )
    beginningOfFriendship = models.DateField(verbose_name="Дата начала дружбы")
    prolog = models.TextField(verbose_name="Пролог")
    text = models.TextField(verbose_name="Текст истории")
    pubDate = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )

    class Meta:
        ordering = ("-beginningOfFriendship",)
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
