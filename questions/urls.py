from django.urls import include, path

from questions.views import QuestionsList, QuestionsTagList

extra_patterns = [
    path("questions/", QuestionsList.as_view(), name="questions"),
    path("questions/tags/", QuestionsTagList.as_view(), name="questions-tags"),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
