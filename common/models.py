from django.db import models
from django.db.models.fields import BooleanField


class City(models.Model):
    # class TimeZone(models.TextChoices):
    #     KALININGRAD = 'Europe/Kaliningrad'
    #     MOSCOW = 'Europe/Moscow'
    #     KIROV = 'Europe/Kirov'
    #     VOLGOGRAD = 'Europe/Volgograd'
    #     ASTRAKHAN = 'Europe/Astrakhan'
    #     'Europe/Saratov', 
    #     'Europe/Ulyanovsk', 
    #     'Europe/Samara', 
    #     'Asia/Yekaterinburg', 
    #     'Asia/Omsk', 
    #     'Asia/Novosibirsk', 
    #     'Asia/Barnaul', 
    #     'Asia/Tomsk', 
    #     'Asia/Novokuznetsk', 
    #     'Asia/Krasnoyarsk', 
    #     'Asia/Irkutsk', 
    #     'Asia/Chita', 
    #     'Asia/Yakutsk', 
    #     'Asia/Khandyga', 
    #     'Asia/Vladivostok', 
    #     'Asia/Ust-Nera', 
    #     'Asia/Magadan', 
    #     'Asia/Sakhalin', 
    #     'Asia/Srednekolymsk', 
    #     'Asia/Kamchatka', 
    #     'Asia/Anadyr'
    name = models.CharField(
        max_length=30,
        verbose_name='Город',
        help_text='Введите город',
    )
    isPrimary = models.BooleanField(
        default=False,
        verbose_name='Приоритет вывода',
        help_text='Укажите, если город должен иметь приоритетный вывод'
    )
    # time_zone = BooleanField

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name
