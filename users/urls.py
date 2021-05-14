from django.urls import path, include
from .views import ProfileView


urlpatterns = [
    path('v1/profile/', ProfileView.as_view()),
]
