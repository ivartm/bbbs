from django.urls import path
from .views import ProfileView
from .views import TokenAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('v1/profile/', ProfileView.as_view()),
    path('v1/token/', TokenAPI.as_view()),
    path('v1/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
]
