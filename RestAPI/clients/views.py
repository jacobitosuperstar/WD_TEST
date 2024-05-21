from base.generic_views import (
    BaseListView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)

from .models import Client


class ClientListView(BaseListView):
    """
    List of Clients
    """
    model = Client
    serializer_depth = 0

class ClientCreationView(BaseCreateView):
    """
    Client Creation
    """
    model = Client
    serializer_depth = 0

class ClientDeatilUpdateDeleteView(
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
):
    """
    Specific Client operations. Get specific client, Update specific client,
    Delete specific client.
    """
    model = Client
    serializer_depth = 0
    url_kwarg = "id"
