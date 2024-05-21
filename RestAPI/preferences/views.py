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
    Notifications getter and updater view.
    """
    model = NotificationPreferences
    serializer_depth = 0
    url_kwarg = "id"
