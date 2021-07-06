from django_filters import rest_framework as filters
from rest_framework.generics import get_object_or_404

from common.exceptions import CityNotSelected
from common.models import City
from entertainment.models import Book, BookTag, Video, VideoTag
from places.models import Place, PlaceTag
from questions.models import Question, QuestionTag
from rights.models import Right, RightTag


class CityRequiredFilterBackend(filters.DjangoFilterBackend):
    """Mandatory filter by city.

    Takes city from request.user for authorized users.
    Takes it from query param for anonymous users.
    """

    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            city = request.user.profile.city
        else:
            city_id = request.query_params.get("city")
            if not city_id:
                raise CityNotSelected
            city = get_object_or_404(City, id=city_id)

        queryset = queryset.filter(city=city)
        return super().filter_queryset(request, queryset, view)


class QuestionFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=QuestionTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Question
        fields = ["tags"]


class RightFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=RightTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Right
        fields = ["tag"]


class PlaceFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=PlaceTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Place
        fields = ["tag"]


class BookFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=BookTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Book
        fields = ["tag"]


class VideoFilter(filters.FilterSet):
    tag = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=VideoTag.objects.all(),
        to_field_name="slug",
    )

    class Meta:
        model = Video
        fields = ["tag"]
