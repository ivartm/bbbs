from django.urls import include, path

from bbbs.story.views import StoryList

extra_patterns = [
    path("story/", StoryList.as_view(), name="stories"),
]

urlpatterns = [
    path("v1/", include(extra_patterns)),
]
