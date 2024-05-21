from typing import Union, Iterable, Optional
import json
from django.http import JsonResponse, HttpRequest, StreamingHttpResponse
from django.views.decorators.http import (
    require_GET,
    require_POST,
)
from django.db.models import Q
from django.conf import settings

from base.http_status_codes import HTTP_STATUS as status
from base.logger import base_logger
from base.generic_views import (
    BaseListView,
    BaseDetailView,
    BaseCreateView,
    BaseUpdateView,
    BaseDeleteView,
)
from preferences.models import NotificationPreferences
from .models import Notifications
from .producer import rabbit_mq_sender


@require_GET
def latest_notification_sender_view(request: HttpRequest):
    """Sends the latest notification to the different users, given their
    notification preferences.
    """
    latest_notification: Optional[Notifications] = Notifications.objects.all().latest("updated_at")

    if not latest_notification:
        base_logger.error("There is no notification to send.")
        return

    user_preferences: Iterable[NotificationPreferences] = NotificationPreferences.objects.all().select_related("client")

    def messages_stream():
        """Clousure to stream the messages sended
        """
        for user in user_preferences:
            if user.email:
                msg = {
                    "message": latest_notification.message,
                    "type": "email",
                    "user_info": user.client.email,
                }
                rabbit_mq_sender(
                    message_data=msg,
                    host=settings.RABBIT_MQ_HOST,
                    port=settings.RABBIT_MQ_PORT,
                    queue_name=msg["type"],
                    routing_key=msg["type"],
                    exchange=msg["type"],
                )
            if user.sms:
                msg = {
                    "message": latest_notification.message,
                    "type": "sms",
                    "user_info": user.client.cellphone,
                }
                rabbit_mq_sender(
                    message_data=msg,
                    host=settings.RABBIT_MQ_HOST,
                    port=settings.RABBIT_MQ_PORT,
                    queue_name=msg["type"],
                    routing_key=msg["type"],
                    exchange=msg["type"],
                )
            data = {
                "user": user.serializer(depth=1),
                "message": latest_notification.message,
            }
            yield json.dumps(data)

    response = StreamingHttpResponse(messages_stream())
    return response


class NotificationsListView(BaseListView):
    """
    List of Notifications
    """
    model = Notifications
    serializer_depth = 0

class NotificationCreationView(BaseCreateView):
    """
    Notification Creation
    """
    model = Notifications
    serializer_depth = 0

class NotificationDeatilUpdateDeleteView(
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
):
    """
    Specific notification operations. Get, Update, Delete, specific
    notifications.
    """
    model = Notifications
    serializer_depth = 0
    url_kwarg = "id"
