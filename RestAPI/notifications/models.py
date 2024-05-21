from django.db import models
from base.models import BaseModel


class Notifications(BaseModel):
    """Email Notification table. Text field because there is no limit of
    characters of format within the mail.
    """
    message = models.TextField()

    class Meta:
        db_table = "notifications"
        verbose_name = "notification"
        verbose_name_plural = "notifications"

    def __str__(self) -> str:
        return f"{self.message}"
