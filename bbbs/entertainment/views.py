from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

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


class ListDetailApiView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass


class ListViewSet(ListModelMixin, GenericViewSet):
    pass


class GuidesView(ListDetailApiView):
    serializer_class = GuideSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Guide.objects.all().order_by("id")
        return queryset


class MoviesTagsView(ListDetailApiView):
    """Returns only MovieTags that used in Video objects."""

    queryset = MovieTag.objects.exclude(movies=None).distinct().order_by("id")
    serializer_class = MovieTagSerializer


class MoviesView(ListDetailApiView):
    permission_classes = [AllowAny]
    serializer_class = MovieSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        queryset = Movie.objects.all().order_by("id")
        return queryset


class VideoTagsView(ListDetailApiView):
    """Returns only VideoTags that used in Video objects."""

    queryset = VideoTag.objects.exclude(videos=None).distinct().order_by("id")
    serializer_class = VideoTagSerializer


class VideoView(ListDetailApiView):
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VideoFilter

    def get_queryset(self):
        queryset = Video.objects.all().order_by("id")
        return queryset


class BooksTagsView(ListViewSet):
    """Returns only BookTags that used in Book objects."""

    queryset = BookTag.objects.exclude(books=None).distinct().order_by("id")
    serializer_class = BookTagSerializer


class BooksView(ListViewSet):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = Book.objects.all().order_by("id")
        return queryset


class ArticlesView(ListDetailApiView):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    def get_queryset(self):
        queryset = Article.objects.all().order_by("id")
        return queryset
