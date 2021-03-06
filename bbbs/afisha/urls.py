from django.urls import include, path
from rest_framework.routers import DefaultRouter

from bbbs.afisha.views import (
    EventAPIView,
    EventParticipantViewSet,
    MonthAPIView,
)

router = DefaultRouter()
router.register(
    "event-participants",
    EventParticipantViewSet,
    basename="event-participants",
)


afisha_urls = [
    path("events/", EventAPIView.as_view(), name="events"),
    path("events/months/", MonthAPIView.as_view(), name="events-months"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/afisha/", include(afisha_urls)),
]
