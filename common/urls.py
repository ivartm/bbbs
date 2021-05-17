from django.urls import path

from .views import CityAPIView


urlpatterns = [
    path('v1/cities/', CityAPIView.as_view()),
]
