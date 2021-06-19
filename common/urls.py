from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CityAPIView, MyCityApiView

router = DefaultRouter()
router.register(
    "my-city",
    MyCityApiView,
    basename="user-city",
)

extra_patterns = [
    path("cities/", CityAPIView.as_view(), name="cities"),
    path("cities/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
