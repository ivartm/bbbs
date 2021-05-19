from django.urls import path
from .views import ProfileView
from .views import TokenAPI

urlpatterns = [
    path('v1/profile/', ProfileView.as_view()),
    path('v1/token/', TokenAPI.as_view())
]
