from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$",
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
