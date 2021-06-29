from rest_framework import generics
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from entertainment.models import (
    Article,
    Book,
    BookTag,
    Guide,
    Movie,
    MovieTag,
    Video,
    VideoTag,
)
from entertainment.serializers import (  # EntertainmentSerializer,
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

    def get_queryset(self):
        queryset = Guide.objects.all().order_by("id")
        return queryset


class MoviesTagsView(ListDetailApiView):
    queryset = MovieTag.objects.all().order_by("id")
    serializer_class = MovieTagSerializer


class MoviesView(ListDetailApiView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all().order_by("id")
        return queryset


class VideosTagsView(ListDetailApiView):
    queryset = VideoTag.objects.all().order_by("id")
    serializer_class = VideoTagSerializer


class VideosView(ListDetailApiView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        queryset = Video.objects.all().order_by("id")
        return queryset


class BooksTagsView(ListViewSet):
    queryset = BookTag.objects.all().order_by("id")
    serializer_class = BookTagSerializer


class BooksView(ListViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all().order_by("id")
        return queryset


class ArticlesView(ListDetailApiView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all().order_by("id")
        return queryset


class EntertainmentList(generics.ListAPIView):
    pass
