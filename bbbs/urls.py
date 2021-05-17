from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/v1/token/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
<<<<<<< HEAD
    path('api/', include('afisha.urls')),
=======
    path('api/', include('common.urls')),
>>>>>>> 8b5c6d7138f28e79baa04f74c5b42fccc2050857
]
