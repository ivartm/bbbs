from django.urls import path, include
from afisha.views import EventViewSet, EventParticipantViewSet
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(
#     'event-participants', EventParticipantViewSet, basename='event-participants'
# )


urlpatterns = [
    path('v1/afisha/events', EventViewSet.as_view(), name='events'),
    # path('v1/afisha', include(router.urls)),
    path('v1/afisha/event-participants', EventParticipantViewSet.as_view(), name='event-participants')
]
