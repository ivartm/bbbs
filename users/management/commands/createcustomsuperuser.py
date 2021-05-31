import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from dotenv import load_dotenv

from common.models import City
from users.models import Profile

load_dotenv()


SUPER_USERNAME = os.getenv("SUPER_USERNAME")
SUPER_FIRST_NAME = os.getenv("SUPER_FIRST_NAME")
SUPER_LAST_NAME = os.getenv("SUPER_LAST_NAME")
SUPER_EMAIL = os.getenv("SUPER_EMAIL")
SUPER_PASSWORD = os.getenv("SUPER_PASSWORD")
SUPER_CITY = os.getenv("SUPER_CITY")
SUPER_TIMEZONE = os.getenv("SUPER_TIMEZONE")


class Command(BaseCommand):
    help = "Создаёт суперпользователя для запуска проекта"

    def handle(self, *args, **options):
        try:
            superuser = User.objects.create(
                username=SUPER_USERNAME,
                first_name=SUPER_FIRST_NAME,
                last_name=SUPER_LAST_NAME,
                email=SUPER_EMAIL,
            )
            superuser.set_password(SUPER_PASSWORD)
            superuser.is_superuser = True
            superuser.is_staff = True
            superuser.save()
            city, createde = City.objects.get_or_create(
                name=SUPER_CITY, isPrimary=True, timeZone=SUPER_TIMEZONE
            )
            city.save()
            profile = Profile.objects.get(user=superuser)
            profile.city = city
            profile.role = "admin"
            profile.save()
            self.stdout.write(f'Пользователь "{superuser.username}" создан')
        except IntegrityError as error:
            self.stderr.write(f"Невозможно создать пользователя: {str(error)}")
