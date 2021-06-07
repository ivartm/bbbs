from django.urls import path, include
from rest_framework.routers import SimpleRouter
from questions.views import QuestionsList, QuestionsTagList


router = SimpleRouter()


router.register('questions-tags', QuestionsTagList, basename='questions-tags')
router.register('questions', QuestionsList, basename='questions')

urlpatterns = [
    path("v1/", include(router.urls)),
]
