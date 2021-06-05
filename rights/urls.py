from django.urls import path

from .views import RightList

urlpatterns = [
    path("v1/rights/", RightList.as_view(), name="right_page"),
]
