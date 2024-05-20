"""
Clients URLs
"""

from django.urls import path
from .views import (
    ClientListView,
    ClientDeatilView,
    ClientCreationView,
    ClientUpdateView,
    ClientDeleteView,
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
        ClientDeatilView.as_view(),
        name="detailed_client",
    ),
    path(
        "<int:id>/update_client/",
        ClientUpdateView.as_view(),
        name="update_client",
    ),
    path(
        "<int:id>/delete_client/",
        ClientDeleteView.as_view(),
        name="delete_client",
    ),
]
