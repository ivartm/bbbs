from django.urls import path
from django.urls.conf import include

from .views import RightList, RightTagList

rights_urls = [
    path("rights/", RightList.as_view(), name="rights"),
    path("rights/tags/", RightTagList.as_view(), name="right-tags"),
]

urlpatterns = [
    path("v1/", include(rights_urls)),
]
