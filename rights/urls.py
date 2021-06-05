from django.urls import path

from .views import RightsList

urlpatterns = [
    path("v1/rights/", RightsList.as_view(), name="rights_page"),
]
