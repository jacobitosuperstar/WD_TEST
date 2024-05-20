"""
Clients URLs
"""

from django.urls import path
from .views import (
    NotificationPreferencesUpdateDeatilView,
)

urlpatterns = [
    path(
        "<int:id>/",
        NotificationPreferencesUpdateDeatilView.as_view(),
        name="detailed_preferences",
    ),
]
