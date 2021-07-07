from colorfield.fields import ColorField
from django.db import models

from common.utils.slugify import slugify


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
        upload_to="entertainment/guides/",
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
    name = models.CharField(
        verbose_name="Название тега", max_length=50, unique=True
    )
    slug = models.SlugField(
        verbose_name="Адрес тега", max_length=50, unique=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-name",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Movie(models.Model):
    tags = models.ManyToManyField(
        MovieTag,
        related_name="movies",
        verbose_name="Теги",
        blank=False,
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название фильма",
    )
    preview = models.ImageField(
        blank=True,
        verbose_name="Картинка к фильму",
        upload_to="entertainment/movies/",
    )
    info = models.TextField(
        verbose_name="Информация о фильме",
    )
    description = models.TextField(
        verbose_name="Описание фильма",
    )
    link = models.TextField(unique=True, verbose_name="Ссылка на фильм")

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["id"]

    def __str__(self):
        return self.title


class VideoTag(models.Model):
    name = models.CharField(
        verbose_name="Название тега", max_length=50, unique=True
    )
    slug = models.SlugField(
        verbose_name="Адрес тега", max_length=50, unique=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег (Видео)"
        verbose_name_plural = "Теги (Видео)"

    def __str__(self):
        return self.name


class Video(models.Model):
    tags = models.ManyToManyField(
        VideoTag,
        blank=False,
        related_name="videos",
    )
    link = models.URLField(
        max_length=250,
        unique=True,
        verbose_name="Ссылка на видео",
    )
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название видео",
    )
    author = models.CharField(max_length=200, verbose_name="Автор")
    pubDate = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    duration = models.DurationField(
        null=True, verbose_name="Продолжительность видео"
    )

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["id"]

    def __str__(self):
        return self.title


class BookTag(models.Model):
    name = models.CharField(
        verbose_name="Название тега", max_length=50, unique=True
    )
    slug = models.SlugField(
        verbose_name="Адрес тега", max_length=50, unique=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег (Книга)"
        verbose_name_plural = "Теги (Книги)"

    def __str__(self):
        return self.name


class Book(models.Model):
    tags = models.ManyToManyField(
        BookTag,
        blank=False,
        related_name="books",
    )
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название книги",
    )
    author = models.CharField(max_length=200, verbose_name="Автор")
    year = models.PositiveSmallIntegerField(verbose_name="Год")
    description = models.TextField(verbose_name="Описание")
    color = ColorField(
        max_length=30,
        verbose_name="Цвет обложки на странице",
    )
    link = models.URLField(
        max_length=250,
        blank=False,
        unique=True,
        verbose_name="Ссылка на книгу",
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["id"]

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название статьи",
    )
    author = models.CharField(max_length=200, verbose_name="Автор")
    profession = models.CharField(max_length=200, verbose_name="Профессия")
    text = models.TextField(verbose_name="Текст")
    color = ColorField(
        max_length=30,
        verbose_name="Цвет обложки на странице",
    )
    imageUrl = models.ImageField(
        blank=True,
        verbose_name="Обложка",
        help_text="Добавить фото",
        upload_to="entertainment/articles/",
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["id"]

    def __str__(self):
        return self.title
