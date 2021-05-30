from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path(
        'api/v1/token/refresh/',
         TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('main.urls')),
    path('api/', include('common.urls')),
    path('api/', include('afisha.urls')),
]


urlpatterns += [
    # YOUR PATTERNS
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    # Optional UI:
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
