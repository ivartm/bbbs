from django.urls import include, path
from rest_framework.routers import DefaultRouter

from afisha.views import EventParticipantViewSet, EventViewSet

router = DefaultRouter()
router.register(
    "event-participants",
    EventParticipantViewSet,
    basename="event-participants",
)


urlpatterns = [
    path("v1/afisha/events/", EventViewSet.as_view(), name="events"),
    path("v1/afisha/", include(router.urls)),
]
