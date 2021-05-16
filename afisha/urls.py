from django.urls import path
from .views import ProfileView


urlpatterns = [
    path('v1/afisha/events', EventView.as_view()),
    path('v1/afisha/event-participants', EventParticipantView.as_view()),
]