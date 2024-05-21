"""Notifications URLs
"""

from django.urls import path
from .views import (
    latest_notification_sender_view,
    NotificationsListView,
    NotificationCreationView,
    NotificationDeatilUpdateDeleteView,
)

urlpatterns = [
    path(
        "",
        latest_notification_sender_view,
        name="notifications_sender",
    ),
    path(
        "list/",
        NotificationsListView.as_view(),
        name="notifications_list",
    ),
    path(
        "create_notification/",
        NotificationCreationView.as_view(),
        name="create_notification",
    ),
    path(
        "<int:id>/",
        NotificationDeatilUpdateDeleteView.as_view(),
        name="detailed_crud_notification",
    ),
]
