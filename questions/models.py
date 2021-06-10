from django.db import models

from common.utils import slugify


class QuestionTag(models.Model):
    name = models.CharField(
        verbose_name="Название тега", max_length=50, unique=True
    )
    slug = models.SlugField(
        verbose_name="Адрес тега", max_length=50, unique=True, editable=False
    )

    class Meta:
        ordering = ("-name",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Question(models.Model):
    tag = models.ManyToManyField(
        QuestionTag,
        verbose_name="Тэги",
        related_name="tags",
        related_query_name="tags",
        blank=True,
    )
    question = models.CharField(
        verbose_name="Вопрос", max_length=500, unique=True
    )
    answer = models.TextField(verbose_name="Ответ на вопрос")
    pubDate = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )

    class Meta:
        ordering = ("-pubDate",)
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def list_tags(self):
        return self.tag.values_list("name")

    def __str__(self):
        return self.question
