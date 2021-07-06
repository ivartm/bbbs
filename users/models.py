from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from common.models import City

User._meta.get_field("email")._unique = True
User._meta.get_field("email").blank = False
User._meta.get_field("email").null = False


class Curator(models.Model):
    FEMALE = "female"
    MALE = "male"

    GENDER_TYPE_CHOICES = [
        (FEMALE, "женский"),
        (MALE, "мужской"),
    ]
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    gender = models.CharField(
        choices=GENDER_TYPE_CHOICES, max_length=10, verbose_name="Пол"
    )
    email = models.EmailField(max_length=25)

    class Meta:
        verbose_name = "Куратор"
        verbose_name_plural = "Кураторы"
        ordering = ("id",)

    def __str__(self):
        return self.email


class Profile(models.Model):
    class Role(models.TextChoices):
        MENTOR = "Наставник", _("Наставник")
        MODERATOR_REG = "Модератор(региональный)", _("Модератор(региональный)")
        MODERATOR_GEN = "Модератор(общий)", _("Модератор(общий)")
        ADMIN = "Администратор", _("Администратор")

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    city = models.ForeignKey(
        City, on_delete=models.RESTRICT, verbose_name="Город"
    )
    region = models.ManyToManyField(
        City,
        blank=True,
        related_name="region",
        verbose_name="Обслуживаемые города",
        related_query_name="region",
    )
    role = models.CharField(
        max_length=25,
        choices=Role.choices,
        default=Role.MENTOR,
        verbose_name="Роль",
    )
    curator = models.ForeignKey(
        Curator,
        on_delete=models.RESTRICT,
        verbose_name="Куратор",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Профиль"

    def __str__(self):
        return f"Дополнительная информация пользователя {self.user.username}"

    def save(self, *args, **kwargs):
        """Two custom things: adds regions if necessary and sync roles.

        1. Add region to moderator_reg if it empty.
        2. Sync Profile role with User role when saving.
        """

        super().save(*args, **kwargs)

        if self.is_moderator_reg and not self.region.exists():
            self.region.add(self.city)

        # if user is superuser don't do anything with is_staff attribute
        if self.user.is_superuser:
            return

        if self.is_mentor:
            self.user.is_staff = False
        else:
            self.user.is_staff = True
        self.user.save()

    @receiver(post_save, sender=User)
    def create_and_update_user_profile(sender, instance, created, **kwargs):
        """Should be analyzed and documented or possibly rewritten.

        Creates Profile object when new user was created. Do nothing if user
        was updated.
        """

        if created:
            obj, city_created = City.objects.get_or_create(
                name="Москва",
                defaults={"name": "Москва", "isPrimary": True},
            )
            if city_created:
                obj.save()

            Profile.objects.create(
                user=instance,
                city=obj,
            )

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator_reg(self):
        return self.role == self.Role.MODERATOR_REG

    @property
    def is_moderator_gen(self):
        return self.role == self.Role.MODERATOR_GEN

    @property
    def is_mentor(self):
        return self.role == self.Role.MENTOR
