from django.contrib import admin
from django.urls import path, include

extra_patterns = [
    path("", include("users.urls")),
    path("", include("main.urls")),
    path("", include("common.urls")),
    path("", include("afisha.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(extra_patterns)),
]
