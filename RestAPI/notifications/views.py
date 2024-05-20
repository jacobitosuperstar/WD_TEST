from base.generic_views import (
    BaseListView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)

from .models import NotificationPreferences


class ClientDeatilView(BaseDetailView):
    """
    Specific Client
    """
    model = NotificationPreferences
    serializer_depth = 0
    url_kwarg = "id"


class ClientUpdateView(BaseUpdateView):
    """
    Client information update
    """
    model = NotificationPreferences
    serializer_depth = 0
    url_kwarg = "id"
