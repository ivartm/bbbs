import pytz
from django.utils import timezone

from common.models import City
from users.models import Profile


def set_timezone(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            if request.user.profile.city == None:  # Noqa
                profile = Profile.objects.get(user=request.user)
                city = City.objects.get(name="Москва")
                profile.city = city
                profile.save()
            timezone.activate(
                pytz.timezone(request.user.profile.city.timeZone)
            )
        else:
            timezone.deactivate()
        return get_response(request)

    return middleware
