from django.urls import include, path

from bbbs.questions.views import QuestionsAPIView, QuestionsTagAPIView

extra_patterns = [
    path(
        route="questions/",
        view=QuestionsAPIView.as_view(),
        name="questions",
    ),
    path(
        route="questions/tags/",
        view=QuestionsTagAPIView.as_view(),
        name="questions-tags",
    ),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
