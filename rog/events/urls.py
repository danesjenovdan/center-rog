from django.urls import path
from events.views import (
    EventRegistrationView,
    EventRegistrationAdditionalView,
)

urlpatterns = [
    path(
        "<slug:event>/posebnosti",
        EventRegistrationAdditionalView.as_view(),
        name="event-registration-additional",
    ),
    path(
        "<slug:event>",
        EventRegistrationView.as_view(),
        name="event-registration",
    ),
]
