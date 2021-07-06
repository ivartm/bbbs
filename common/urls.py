from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CityAPIView, MeetingAPIView, MyCityApiView

router = DefaultRouter()
router.register(
    "cities/my-city",
    MyCityApiView,
    basename="user-city",
)

router.register(
    "meetings",
    MeetingAPIView,
    basename="meetings",
)

extra_patterns = [
    path("cities/", CityAPIView.as_view(), name="cities"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
