import pytz
from django.utils import timezone

from common.models import City
from users.models import Profile


def set_timezone(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            if request.user.profile.city == None:  # Noqa
                city, created = City.objects.get_or_create(
                    name='Москва',
                    isPrimary=True,
                    timeZone="Europe/Moscow"
                )
                Profile.objects.filter(user=request.user).update(city=city)
            timezone.activate(
                pytz.timezone(request.user.profile.city.timeZone)
            )
        else:
            timezone.deactivate()
        return get_response(request)

    return middleware
