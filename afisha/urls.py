from django.urls import include, path
from rest_framework.routers import DefaultRouter

from afisha.views import EventAPIView, EventParticipantViewSet

router = DefaultRouter()
router.register(
    "event-participants",
    EventParticipantViewSet,
    basename="event-participants",
)


afisha_urls = [
    path("events/", EventAPIView.as_view(), name="events"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("v1/afisha/", include(afisha_urls)),
]
