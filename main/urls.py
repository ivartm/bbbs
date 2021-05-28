from django.urls import path

from .views import MainView


urlpatterns = [
    path("v1/main/", MainView.as_view(), name="main_page"),
]
