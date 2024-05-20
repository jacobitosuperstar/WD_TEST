from base.generic_views import (
    BaseDetailView,
    BaseUpdateView,
)

from .models import NotificationPreferences


class NotificationPreferencesUpdateDeatilView(
    BaseDetailView,
    BaseUpdateView,
):
    """
    Specific Client
    """
    model = NotificationPreferences
    serializer_depth = 0
    url_kwarg = "id"
