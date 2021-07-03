from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from rights.views import RightViewSet, RightTagList

router = DefaultRouter()
router.register("rights", RightViewSet, basename="rights")

rights_urls = [
    path("rights/tags/", RightTagList.as_view(), name="right-tags"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(rights_urls)),
]
