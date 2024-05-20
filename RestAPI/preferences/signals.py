"""Signals of user preferences."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from clients.models import Client
from .models import NotificationPreferences

@receiver(post_save, sender=Client)
def create_client_preferences(
    sender,
    instance: Client,
    created: bool,
    **kwargs,
):
    if created:
        preferences = NotificationPreferences(client=instance)
        preferences.save()
    return
