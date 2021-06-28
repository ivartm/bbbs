from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static

DEBUG = settings.DEBUG

extra_patterns = [
    path("", include("users.urls")),
    path("", include("main.urls")),
    path("", include("common.urls")),
    path("", include("afisha.urls")),
    path("", include("places.urls")),
    path("", include("questions.urls")),
    path("", include("rights.urls")),
    path("", include("entertainment.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(extra_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


schema_view = get_schema_view(
    openapi.Info(
        title="bbbs API",
        default_version="v1",
        contact=openapi.Contact(email="contact@snippets.local"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path(
        "swagger<str:format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
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
