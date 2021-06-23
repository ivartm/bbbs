from django.urls import include, path

from .views import PlacesAPIView, PlacesTagAPIView

extra_patterns = [
    path("places/tags/", PlacesTagAPIView.as_view(), name="places-tags"),
    path("places/", PlacesAPIView.as_view(), name="places"),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
