import urllib

from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models

from common.utils.slugify import slugify
from common.utils.youtube_api import get_youtube_data


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
    image_caption = models.CharField(
        max_length=200,
        verbose_name="Описание к фотографии",
    )
    image_url = models.ImageField(
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
        verbose_name="Название тега", max_length=50, unique=True, null=True
    )
    slug = models.SlugField(
        verbose_name="Адрес тега", max_length=50, unique=True, null=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег (Фильмы)"
        verbose_name_plural = "Теги (Фильмы)"

    def __str__(self):
        return self.name


class Movie(models.Model):
    tags = models.ManyToManyField(
        MovieTag,
        related_name="movies",
        verbose_name="Теги",
        blank=False,
    )
    link = models.URLField(
        verbose_name="Ссылка на фильм",
        null=True,
        blank=False,
        max_length=250,
    )
    title = models.CharField(
        blank=True,
        max_length=100,
        unique=True,
        verbose_name="Название фильма",
    )
    producer = models.CharField(
        verbose_name="Режиссер", max_length=255, blank=True
    )
    year = models.PositiveSmallIntegerField(verbose_name="Год", blank=True)
    description = models.TextField(verbose_name="Описание фильма", blank=True)
    image_url = models.ImageField(
        blank=True,
        verbose_name="Картинка к видео",
        upload_to="entertainment/movies/",
    )
    duration = models.DurationField(
        null=True, blank=True, verbose_name="Продолжительность фильма"
    )

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["id"]

    def __str__(self):
        return self.title

    def clean(self):
        if "youtube.com" not in self.link:
            raise ValidationError("Ссылка должна быть с youtube.com")

    def save(self, *args, **kwargs):
        data = get_youtube_data(self.link)
        if not self.title:
            self.title = data["title"]
        if not self.producer:
            self.producer = data["author"]
        if not self.image_url:
            content = urllib.request.urlopen(data["preview"]).read()
            self.image_url.save(
                data["video_id"] + ".jpg", ContentFile(content), save=False
            )
        if not self.year:
            year = data["date"].split("-")
            self.year = year[0]
        if not self.description:
            self.description = data["description"]
        self.duration = data["duration"]
        super().save(*args, **kwargs)


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
        VideoTag, blank=False, related_name="videos", verbose_name="Тэги"
    )
    link = models.URLField(
        max_length=250,
        unique=True,
        verbose_name="Ссылка на видео",
    )
    title = models.CharField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name="Название видео",
    )
    author = models.CharField(max_length=200, verbose_name="Автор", blank=True)
    pub_date = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    image_url = models.ImageField(
        blank=True,
        verbose_name="Картинка к видео",
        upload_to="entertainment/videos/",
    )
    creative_url = models.CharField(blank=True, max_length=250)
    duration = models.DurationField(
        null=True, verbose_name="Продолжительность видео"
    )

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        data = get_youtube_data(self.link)
        if self.title == "":
            self.title = data["title"]
        if self.author == "":
            self.author = data["author"]
        self.creative_url = data["preview"]
        content = urllib.request.urlopen(self.creative_url).read()
        if self.image_url == "":
            self.image_url.save(
                data["video_id"] + ".jpg", ContentFile(content), save=False
            )
        self.duration = data["duration"]
        super().save(*args, **kwargs)

    def clean(self):
        if "youtube.com" not in self.link:
            raise ValidationError("Ссылка должна быть с youtube.com")


class BookTag(models.Model):
    name = models.CharField(
        verbose_name="Название тега", max_length=50, unique=True
    )
    slug = models.SlugField(
        verbose_name="Адрес тега", max_length=50, unique=True
    )
    COLOR_CHOICES = [("#FF8484", "red"), ("#C8D1FF", "violet")]
    color = ColorField(
        max_length=8,
        verbose_name="Цвет обложки на странице",
        choices=COLOR_CHOICES,
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
    tag = models.ForeignKey(
        BookTag,
        blank=False,
        on_delete=models.CASCADE,
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

    is_main = models.BooleanField(
        verbose_name="Основная статья",
        default=False,
    )
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название статьи",
    )
    author = models.CharField(max_length=200, verbose_name="Автор")
    profession = models.CharField(max_length=200, verbose_name="Профессия")
    description = models.TextField(verbose_name="Описание")
    text = models.TextField(verbose_name="Текст")
    COLOR_CHOICES = [
        ("#F8D162", "yellow"),
        ("#8CDD94", "green"),
        ("#FF8484", "pink"),
        ("#C8D1FF", "blue"),
    ]
    color = ColorField(
        max_length=8,
        verbose_name="Цвет обложки на странице",
        choices=COLOR_CHOICES,
    )
    image_url = models.ImageField(
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

    def clean(self):
        is_main = Article.objects.filter(is_main=True).first()
        if is_main != self and self.is_main and is_main:
            raise ValidationError(
                "Чтобы выбрать данную статью, "
                "необходимо деактивировать "
                f"статью №{is_main.pk}"
            )

    def save(self, *args, **kwargs):
        is_main = Article.objects.filter(is_main=True)
        if is_main.exists() and is_main.first() != self:
            self.is_main = False
        super().save(*args, **kwargs)
