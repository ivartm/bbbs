from django.db import models


class City(models.Model):
    KALININGRAD = "Europe/Kaliningrad"
    MOSCOW = "Europe/Moscow"
    KIROV = "Europe/Kirov"
    VOLGOGRAD = "Europe/Volgograd"
    ASTRAKHAN = "Europe/Astrakhan"
    SARATOV = "Europe/Saratov"
    ULYANOVSK = "Europe/Ulyanovsk"
    SAMARA = "Europe/Samara"
    YEKATERINBURG = "Asia/Yekaterinburg"
    OMSK = "Asia/Omsk"
    NOVOSIBIRSK = "Asia/Novosibirsk"
    BARNAUL = "Asia/Barnaul"
    TOMSK = "Asia/Tomsk"
    NOVOKUZNETSK = "Asia/Novokuznetsk"
    KRASNOYARSK = "Asia/Krasnoyarsk"
    IRKUTSK = "Asia/Irkutsk"
    CHITA = "Asia/Chita"
    YAKUTSK = "Asia/Yakutsk"
    KHANDYGA = "Asia/Khandyga"
    VLADIVOSTOK = "Asia/Vladivostok"
    UST_NERA = "Asia/Ust-Nera"
    MAGADAN = "Asia/Magadan"
    SAKHALIN = "Asia/Sakhalin"
    SREDNEKOLYMSK = "Asia/Srednekolymsk"
    KAMCHATKA = "Asia/Kamchatka"
    ANADYR = "Asia/Anadyr"
    TIMEZONE_CHOICES = [
        (KALININGRAD, "Калининград"),
        (MOSCOW, "Москва"),
        (KIROV, "Киров"),
        (VOLGOGRAD, "Волгоград"),
        (ASTRAKHAN, "Астрахань"),
        (SARATOV, "Саратов"),
        (ULYANOVSK, "Ульяновск"),
        (SAMARA, "Самара"),
        (YEKATERINBURG, "Екатеринбург"),
        (OMSK, "Омск"),
        (NOVOSIBIRSK, "Новосибирск"),
        (BARNAUL, "Барнаул"),
        (TOMSK, "Томск"),
        (NOVOKUZNETSK, "Новокузнецк"),
        (KRASNOYARSK, "Красноярск"),
        (IRKUTSK, "Иркутск"),
        (CHITA, "Чита"),
        (YAKUTSK, "Якутск"),
        (KHANDYGA, "Хандыга"),
        (VLADIVOSTOK, "Владивосток"),
        (UST_NERA, "Усть-Нера"),
        (MAGADAN, "Магадан"),
        (SAKHALIN, "Сахалин"),
        (SREDNEKOLYMSK, "Среднеколымск"),
        (KAMCHATKA, "Камчатка"),
        (ANADYR, "Анадырь"),
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
