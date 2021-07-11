from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from entertainment.views import (
    ArticlesView,
    BooksTagsView,
    BooksView,
    GuidesView,
    MoviesTagsView,
    MoviesView,
    VideoTagsView,
    VideoView,
)

router = DefaultRouter()
router.register("guides", GuidesView, basename="guides")
router.register("movies/tags", MoviesTagsView, basename="movies-tags")
router.register("movies", MoviesView, basename="movies")
router.register("videos/tags", VideoTagsView, basename="videos-tags")
router.register("videos", VideoView, basename="videos")
router.register("books/tags", BooksTagsView, basename="books-tag")
router.register("books", BooksView, basename="books")
router.register("articles", ArticlesView, basename="articles")

entertainment_urls = [
    path("entertainment/", include(router.urls)),
]

urlpatterns = [
    path("v1/", include(entertainment_urls)),
]
