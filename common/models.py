from django.db import models


class City(models.Model):
    KALININGRAD = "Europe/Kaliningrad"
    MOSCOW = "Europe/Moscow"
    SAMARA = "Europe/Samara"
    YEKATERINBURG = "Asia/Yekaterinburg"
    OMSK = "Asia/Omsk"
    KRASNOYARSK = "Asia/Krasnoyarsk"
    IRKUTSK = "Asia/Irkutsk"
    YAKUTSK = "Asia/Yakutsk"
    VLADIVOSTOK = "Asia/Vladivostok"
    SREDNEKOLYMSK = "Asia/Srednekolymsk"
    KAMCHATKA = "Asia/Kamchatka"
    TIMEZONE_CHOICES = [
        (KALININGRAD, "Калининградское время GMT-1"),
        (MOSCOW, "Московское время GMT+0"),
        (SAMARA, "Самарское время GMT+1"),
        (YEKATERINBURG, "Екатеринбургское время GMT+2"),
        (OMSK, "Омское время GMT+3"),
        (KRASNOYARSK, "Красноярское время GMT+4"),
        (IRKUTSK, "Иркутское время GMT+5"),
        (YAKUTSK, "Якутское время GMT+6"),
        (VLADIVOSTOK, "Владивостокское время GMT+7"),
        (SREDNEKOLYMSK, "Среднеколымское время GMT+8"),
        (KAMCHATKA, "Камчатское время GMT+9"),
    ]
    name = models.CharField(
        max_length=30,
        verbose_name="Город",
        help_text="Введите город",
        unique=True,
    )
    isPrimary = models.BooleanField(
        default=False,
        verbose_name="Приоритет вывода",
        help_text="Укажите, если город должен иметь приоритетный вывод",
    )
    timeZone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default=MOSCOW,
        verbose_name="Часовой пояс",
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
