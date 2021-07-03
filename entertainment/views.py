# from rest_framework import generics
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from common.filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

# from rest_framework.response import Response


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
    # EntertainmentSerializer
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
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = Book.objects.all().order_by("id")
        return queryset


class ArticlesView(ListDetailApiView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all().order_by("id")
        return queryset


# class EntertainmentList(generics.ListAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = EntertainmentSerializer

#     def get_queryset(self):
#         context = {}
#         guides = GuidesView.get_queryset(self)
#         context.update(**guides)
# return Response(context)
