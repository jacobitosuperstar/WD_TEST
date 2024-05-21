"""
Clients URLs
"""

from django.urls import path
from .views import (
    ClientListView,
    ClientCreationView,
    ClientDeatilUpdateDeleteView,
)

urlpatterns = [
    path(
        "",
        ClientListView.as_view(),
        name="clients_list",
    ),
    path(
        "create_client/",
        ClientCreationView.as_view(),
        name="create_client",
    ),
    path(
        "<int:id>/",
        ClientDeatilUpdateDeleteView.as_view(),
        name="detailed_crud_client",
    ),
]
