from django.urls import path
from django.urls.conf import include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ProfileView, TokenAPI

extra_patterns = [
    path("token/", TokenAPI.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
