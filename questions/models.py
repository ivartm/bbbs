from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Question(models.Model):
    tag = models.ManyToManyField(
        Tag,
        related_name="tags",
        blank=True,
    )
    question = models.CharField(max_length=500, unique=True)
    answer = models.TextField(verbose_name="Ответ на вопрос")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def list_tags(self):
        return self.tag.values_list("name")

    def __str__(self):
        return self.question
