from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

DEBUG = settings.DEBUG

extra_patterns = [
    path("", include("users.urls")),
    path("", include("main.urls")),
    path("", include("common.urls")),
    path("", include("afisha.urls")),
    path("", include("places.urls")),
    path("", include("questions.urls")),
    path("", include("rights.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(extra_patterns)),
]

urlpatterns += [
    # YOUR PATTERNS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

admin.site.site_header = "Панель администраторов"
admin.site.site_title = "Наставники.про"
admin.site.index_title = "Добро пожаловать на портал Наставники.про"
