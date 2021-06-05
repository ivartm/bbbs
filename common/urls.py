from django.urls import path, include

from .views import CityAPIView, MyCityApiView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(
    "my-city",
    MyCityApiView,
    basename="user-city",
)

extra_patterns = [
    path("cities/", CityAPIView.as_view(), name="cities"),
    path("tags/", TagList.as_view()),
    path("cities/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
