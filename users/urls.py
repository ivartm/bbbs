from django.urls import path
from django.urls.conf import include
from .views import ProfileView
from .views import TokenAPI
from rest_framework_simplejwt.views import TokenRefreshView

extra_patterns = [
    path("token/", TokenAPI.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
