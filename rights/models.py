from colorfield.fields import ColorField
from django.db import models


class RightTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

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
    text = models.TextField(
        verbose_name="Основной текст права ребенка",
    )
    color = ColorField(
        verbose_name="Цвет обложки на странице",
    )
    imageUrl = models.ImageField(
        blank=True,
        verbose_name="Фото",
        help_text="Добавить фото",
        upload_to="rights/",
    )
    tag = models.ManyToManyField(
        "RightTag",
        blank=True,
        related_name="tags",
    )

    class Meta:
        verbose_name = "Право ребенка"
        verbose_name_plural = "Права детей"

    def __str__(self):
        return self.title
