from django.urls import path
from afisha.views import (
    EventViewSet,
    EventParticipantGetPostViewSet,
    EventParticipantDeleteViewSet,
)
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(
#     "event-participants/<int:pk>",
#     EventParticipantViewSet,
#     basename="participants",
# )


urlpatterns = [
    path("v1/afisha/events/", EventViewSet.as_view(), name="events"),
    # path('v1/afisha/', include(router.urls)),
    path(
        "v1/afisha/event-participants/",
        EventParticipantGetPostViewSet.as_view(
            {"get": "list", "post": "create"}
        ),
        name="event-participants",
    ),
    path(
        "v1/afisha/event-participants/<int:pk>",
        EventParticipantDeleteViewSet.as_view({"delete": "destroy"}),
        name="event-participants-pk",
    ),
]
