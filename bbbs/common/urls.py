from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CityAPIView, MeetingViewSet

router = DefaultRouter()

router.register(
    prefix="meetings",
    viewset=MeetingViewSet,
    basename="meetings",
)

extra_patterns = [
    path("cities/", CityAPIView.as_view(), name="cities"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
