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

class ClientDeatilView(BaseDetailView):
    """
    Specific Client
    """
    model = Client
    serializer_depth = 0
    url_kwarg = "id"

class ClientCreationView(BaseCreateView):
    """
    Client Creation
    """
    model = Client
    serializer_depth = 0

class ClientUpdateView(BaseUpdateView):
    """
    Client information update
    """
    model = Client
    serializer_depth = 0
    url_kwarg = "id"

class ClientDeleteView(BaseDeleteView):
    """
    Client soft delete
    """
    model = Client
    serializer_depth = 0
    url_kwarg = "id"
