from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from bbbs.entertainment.filters import (
    ArticleFilter,
    BookFilter,
    MovieFilter,
    VideoFilter,
)
from bbbs.entertainment.models import (
    Article,
    Book,
    BookTag,
    Guide,
    Movie,
    MovieTag,
    Video,
    VideoTag,
)
from bbbs.entertainment.serializers import (
    ArticleSerializer,
    BookSerializer,
    BookTagSerializer,
    GuideSerializer,
    MovieSerializer,
    MovieTagSerializer,
    VideoSerializer,
    VideoTagSerializer,
)


class ListViewSet(ListModelMixin, GenericViewSet):
    pass


class GuidesViewSet(ReadOnlyModelViewSet):
    serializer_class = GuideSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Guide.objects.all().order_by("id")
        return queryset


class MoviesTagsViewSet(ListViewSet):

    """Returns only MovieTags that used in Video objects."""

    permission_classes = [AllowAny]
    queryset = MovieTag.objects.exclude(movies=None).distinct().order_by("id")
    serializer_class = MovieTagSerializer


class MoviesViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = MovieSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        queryset = Movie.objects.all().order_by("id")
        return queryset


class VideoTagsViewSet(ListViewSet):
    """Returns only VideoTags that used in Video objects."""

    permission_classes = [AllowAny]
    queryset = VideoTag.objects.exclude(videos=None).distinct().order_by("id")
    serializer_class = VideoTagSerializer


class VideoViewSet(ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VideoFilter

    def get_queryset(self):
        queryset = Video.objects.all().order_by("id")
        return queryset


class BooksTagsViewSet(ListViewSet):
    """Returns only BookTags that used in Book objects."""

    permission_classes = [AllowAny]
    queryset = BookTag.objects.exclude(books=None).distinct().order_by("id")
    serializer_class = BookTagSerializer


class BooksViewSet(ReadOnlyModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = Book.objects.all().order_by("id")
        return queryset


class ArticlesViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    def get_queryset(self):
        queryset = Article.objects.all().order_by("id")
        return queryset
