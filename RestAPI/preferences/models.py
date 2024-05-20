from django.db import models

from base.models import BaseModel
from clients.models import Client


class NotificationPreferences(BaseModel):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    email = models.BooleanField(default=False)
    sms = models.BooleanField(default=False)

    class Meta:
        db_table = "notification_preferences"
        verbose_name = "notification_preferences"
        verbose_name_plural = "notification_preferences"

    def __str__(self) -> str:
        return f"{self.client.id}"
