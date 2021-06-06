from django.urls import path

from .views import PlaceList

urlpatterns = [
    path("v1/place/", PlaceList.as_view(), name="place_page"),
]
