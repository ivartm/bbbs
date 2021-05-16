from django.db import models
from django.conf import settings
from common.models import City


class Profile(models.Model):
    class Role(models.TextChoices):
        MENTOR = "mentor"
        MODERATOR_REG = "moderator_regional"
        MODERATOR_GEN = "moderator_general"
        ADMIN = "admin"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    city = models.OneToOneField(City, on_delete=models.RESTRICT)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )

    def __str__(self):
        return "Профиль пользователя {}".format(self.user.username)

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
