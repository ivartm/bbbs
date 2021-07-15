from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.views import error400, error404, error500

DEBUG = settings.DEBUG

handler400 = error400
handler404 = error404
handler500 = error500

extra_patterns = [
    path("", include("bbbs.users.urls")),
    path("", include("bbbs.main.urls")),
    path("", include("bbbs.common.urls")),
    path("", include("bbbs.afisha.urls")),
    path("", include("bbbs.places.urls")),
    path("", include("bbbs.questions.urls")),
    path("", include("bbbs.rights.urls")),
    path("", include("bbbs.entertainment.urls")),
    path("", include("bbbs.story.urls")),
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

admin.site.site_header = "Панель администраторов"
admin.site.site_title = "Наставники.про"
admin.site.index_title = "Добро пожаловать на портал Наставники.про"

if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
