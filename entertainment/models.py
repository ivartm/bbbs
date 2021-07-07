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
    pass


class Video(models.Model):
    pass


class BookTag(models.Model):
    pass


class Book(models.Model):
    pass


class Article(models.Model):
    pass
