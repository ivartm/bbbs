from django.db import models
from django.utils.translation import gettext_lazy

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
    class Colors(models.TextChoices):
        YELLOW = "#E9D379", gettext_lazy("Жёлтый")
        GREEN = "#AAD59E", gettext_lazy("Зелёный")
        PINK = "#DF9687", gettext_lazy("Розовый")
        BLUE = "#CDD2FA", gettext_lazy("Голубой")

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Право ребенка",
    )
    description = models.CharField(
        max_length=500,
        verbose_name="Описание права ребенка",
    )
    color = models.CharField(
        verbose_name="Цвет фигуры",
        max_length=8,
        choices=Colors.choices,
        default="#E9D379",
    )
    text = models.TextField(
        verbose_name="1 текст права ребенка",
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
