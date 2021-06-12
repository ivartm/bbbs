from colorfield.fields import ColorField
from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from common.utils import slugify

from common.utils import slugify


class RightTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name", "slug"]
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

    def __str__(self):
        return self.title

    @property
    @admin.display(
        description="Цвет блока",
    )
    def colored_circle(self):
        return format_html(
            "<span style='"
            "height: 25px;"
            "width: 25px;"
            "border: 1px solid grey;"
            "border-radius: 50%;"
            "display: inline-block;"
            "background-color: {};'>"
            "</span>",
            self.color,
        )

    class Meta:
        ordering = ["title", "id"]
        verbose_name = "Право ребенка"
        verbose_name_plural = "Права детей"
