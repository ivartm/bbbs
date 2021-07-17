from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from bbbs.entertainment.views import (
    ArticlesViewSet,
    BooksTagsViewSet,
    BooksViewSet,
    GuidesViewSet,
    MoviesTagsViewSet,
    MoviesViewSet,
    VideoTagsViewSet,
    VideoViewSet,
)

router = DefaultRouter()
router.register("guides", GuidesViewSet, basename="guides")
router.register("movies/tags", MoviesTagsViewSet, basename="movies-tags")
router.register("movies", MoviesViewSet, basename="movies")
router.register("videos/tags", VideoTagsViewSet, basename="videos-tags")
router.register("videos", VideoViewSet, basename="videos")
router.register("books/tags", BooksTagsViewSet, basename="books-tags")
router.register("books", BooksViewSet, basename="books")
router.register("articles", ArticlesViewSet, basename="articles")

entertainment_urls = [
    path("entertainment/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(entertainment_urls)),
]
