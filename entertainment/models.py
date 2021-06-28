from django.db import models


class Guide(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название статьи",
    )
    description = models.CharField(
        max_length=500,
        verbose_name="Описание статьи",
    )
    imageCaption = models.CharField(
        max_length=200,
        verbose_name="Описание к фотографии",
    )
    imageUrl = models.ImageField(
        blank=True,
        verbose_name="Фото статьи",
        help_text="Добавить фото",
        upload_to="entertainment/manual/",
    )
    text = models.TextField(
        verbose_name="Текст статьи",
    )

    class Meta:
        verbose_name = "Статья справочника"
        verbose_name_plural = "Статьи справочника"
        ordering = ["id"]

    def __str__(self):
        return self.title


class MovieTag(models.Model):
    pass


class Movie(models.Model):
    pass


class VideoTag(models.Model):
    pass


class Video(models.Model):
    pass


class BookTag(models.Model):
    pass


class Book(models.Model):
    pass


class Article(models.Model):
    pass
