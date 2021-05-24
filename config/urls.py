from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/v1/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('main.urls')),
    path('api/', include('common.urls')),
    path('api/', include('afisha.urls')),
]
