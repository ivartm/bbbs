from django.urls import path, include

from .views import CityAPIView, MyCityApiView


extra_patterns = [
    path('cities/', CityAPIView.as_view(), name='cities'),
    path(
        'cities/my-city/',
        MyCityApiView.as_view({'get': 'list'}),
        name='user_city'
    ),
    path(
        'cities/my-city/<int:pk>',
        MyCityApiView.as_view({'put': 'update'}),
        name='update_user_city'
    )
]


urlpatterns = [
    path('v1/', include(extra_patterns)),
]
