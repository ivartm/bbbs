from django.db import models

from common.utils.slugify import slugify


class RightTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег (права детей)"
        verbose_name_plural = "Теги (права детей)"

    def __str__(self):
        return self.name


class Right(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Право ребенка",
    )
    description = models.CharField(
        max_length=500,
        verbose_name="Описание права ребенка",
    )
    heading1 = models.CharField(
        max_length=200,
        null=True,
        verbose_name="Заголовок 1",
    )
    heading2 = models.CharField(
        max_length=200,
        null=True,
        verbose_name="Заголовок 2",
    )
    heading3 = models.CharField(
        max_length=200,
        null=True,
        verbose_name="Заголовок 3",
    )
    heading4 = models.CharField(
        max_length=200,
        null=True,
        verbose_name="Заголовок 4",
    )
    heading5 = models.CharField(
        max_length=200,
        null=True,
        verbose_name="Заголовок 5",
    )
    text1 = models.TextField(
        verbose_name="1 текст права ребенка",
        null=True,
    )
    text2 = models.TextField(
        verbose_name="2 текст права ребенка",
        null=True,
    )
    text3 = models.TextField(
        verbose_name="3 текст права ребенка",
        null=True,
    )
    text4 = models.TextField(
        verbose_name="4 текст права ребенка",
        null=True,
    )
    text5 = models.TextField(
        verbose_name="5 текст права ребенка",
        null=True,
    )
    image_url = models.ImageField(
        blank=True,
        verbose_name="Фото",
        help_text="Добавить фото",
        upload_to="rights/",
    )
    tags = models.ManyToManyField(
        "RightTag",
        blank=False,
        related_name="rights",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title", "id"]
        verbose_name = "Право ребенка"
        verbose_name_plural = "Права детей"
