from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PlacesTagAPIView, PlacesViewSet

router = DefaultRouter()

router.register(
    prefix="places",
    viewset=PlacesViewSet,
    basename="places",
)

extra_patterns = [
    path("places/tags/", PlacesTagAPIView.as_view(), name="places-tags"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
