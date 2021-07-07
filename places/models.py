from django.db import models
from django.utils.translation import gettext_lazy

from common.models import City
from common.utils.slugify import slugify


class PlaceTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег (места: куда пойти?)"
        verbose_name_plural = "Теги (места: куда пойти?)"

    def __str__(self):
        return self.name


class Place(models.Model):
    class Genders(models.TextChoices):
        MALE = "M", gettext_lazy("Мальчик")
        FEMALE = "F", gettext_lazy("Девочка")

    class ActivityTypes(models.IntegerChoices):
        ACTIVE = 0, gettext_lazy("Активный")
        ENTERTAINING = 1, gettext_lazy("Развлекательный")
        INFORMATIVE = 2, gettext_lazy("Познавательный")

    chosen = models.BooleanField(
        verbose_name="Выбор наставника",
        default=False,
    )
    published = models.BooleanField(
        verbose_name="Отображение на странице",
        default=False,
    )
    title = models.CharField(
        verbose_name="Название", max_length=200, null=False, blank=False
    )
    address = models.CharField(
        verbose_name="Адрес", max_length=200, null=False, blank=False
    )
    city = models.ForeignKey(
        City,
        related_name="places",
        on_delete=models.CASCADE,
        verbose_name="Город",
    )
    gender = models.CharField(
        verbose_name="Пол",
        choices=Genders.choices,
        max_length=1,
        null=True,
        blank=True,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Возраст", null=False, blank=False
    )
    activity_type = models.PositiveSmallIntegerField(
        verbose_name="Тип отдыха",
        choices=ActivityTypes.choices,
    )
    description = models.TextField(
        verbose_name="Комментарий",
        help_text="Поделитесь впечатлениями о проведенном времени",
    )
    link = models.URLField(
        verbose_name="Сайт",
        help_text="Введите адрес сайта",
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        PlaceTag, related_name="places", blank=False, verbose_name="Теги"
    )
    imageUrl = models.ImageField(
        verbose_name="Фото",
        help_text="Добавить фото",
        null=True,
        blank=True,
        upload_to="places/",
    )

    class Meta:
        verbose_name = "Место - куда пойти?"
        verbose_name_plural = "Места - куда пойти?"
        ordering = ("id",)

    def __str__(self):
        return self.title

    def list_tags(self):
        return self.tag.values_list("name")

    def get_gender(self, gender_code):
        return self.Genders(gender_code).label

    def get_activity_type(self, type_code):
        return self.ActivityTypes(type_code).label
