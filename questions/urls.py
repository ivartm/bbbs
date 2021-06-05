from django.urls import path

from .views import QuestionsList

urlpatterns = [
    path("v1/question/", QuestionsList.as_view(), name="question_page"),
]
