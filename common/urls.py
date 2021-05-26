from django.urls import path

from .views import CityAPIView, MyCityApiView


urlpatterns = [
    path('v1/cities/', CityAPIView.as_view(), name='cities'),
    path('v1/cities/my-city/', MyCityApiView.as_view({'get': 'list'})),
    path(
        'v1/cities/my-city/<int:pk>', MyCityApiView.as_view({'put': 'update'})
    )
]
