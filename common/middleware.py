import pytz
from django.utils import timezone


def set_timezone(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                timezone.activate(pytz.timezone('UTC'))
            else:
                timezone.activate(
                    pytz.timezone(request.user.profile.city.timeZone)
                )
        else:
            timezone.deactivate()
        return get_response(request)

    return middleware
