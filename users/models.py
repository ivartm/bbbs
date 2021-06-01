from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from common.models import City


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
        City, on_delete=models.SET_NULL, null=True, verbose_name="Город"
    )
    role = models.CharField(
        max_length=25,
        choices=Role.choices,
        default=Role.MENTOR,
        verbose_name="Роль",
    )

    class Meta:
        verbose_name = "Профиль"

    def __str__(self):
        return f"Дополнительная информация пользователя {self.user.username}"

    @receiver(post_save, sender=User)
    def create_and_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @property
    def is_admin(self):
        return self.Role.ADMIN == self.role

    @property
    def is_moderator_reg(self):
        return self.Role.MODERATOR_REG == self.role

    @property
    def is_moderator_gen(self):
        return self.Role.MODERATOR_GEN == self.role

    @property
    def is_mentor(self):
        return self.Role.MENTOR == self.role
