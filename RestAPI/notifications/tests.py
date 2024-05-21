import json
from django.test import (
    TestCase,
    Client as ServerClient,
)
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status

from clients.models import Client
from preferences.models import NotificationPreferences
from notifications.models import Notifications


class ClientsWorkflowTest(TestCase):
    """
    Set of test cases for listing, getting, creating, updating and deleting
    notifications.
    """
    def setUp(self):
        self.client = ServerClient()
        return


    def test_create_get_notifications(self):
        """
        Test flow for the creation of a notification and check that the
        information passed is being recorded in the database.
        """
        # Create a notification
        msg = {
            "message": "Nothing but a test notification.",
        }
        response = self.client.post(
            reverse(viewname="create_notification"),
            data=json.dumps(msg),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.created)
        created_notification = json.loads(response.content)
        self.assertEqual(
            msg["message"],
            created_notification["notification"]["message"],
        )

        # listing all the notifications
        response = self.client.get(
            reverse(viewname="notifications_list")
        )
        self.assertEqual(response.status_code, status.ok)

        # get an specific client
        response = self.client.get(
            reverse(
                viewname="detailed_crud_notification",
                args=[created_notification["notification"]["id"]],
            ),
        )
        self.assertEqual(response.status_code, status.accepted)
        specific_notification = json.loads(response.content)
        self.assertEqual(
            created_notification["notification"]["id"],
            specific_notification["notification"]["id"]
        )


    def test_create_update_delete_client(self):
        """
        Test flow for the creation, update and soft deletion of a notification.
        """
        # Create a notification
        msg = {
            "message": "Nothing but a test notification.",
        }
        response = self.client.post(
            reverse(viewname="create_notification"),
            data=json.dumps(msg),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.created)
        created_notification = json.loads(response.content)
        self.assertEqual(
            msg["message"],
            created_notification["notification"]["message"],
        )

        # Update a Notification
        new_msg = {
            "message": "Nothing but an updated test notification.",
        }

        response = self.client.post(
            reverse(
                viewname="detailed_crud_notification",
                args=[created_notification["notification"]["id"]],
            ),
            data=json.dumps(new_msg),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.accepted)
        updated_notification = json.loads(response.content)
        self.assertEqual(
            new_msg["message"],
            updated_notification["notification"]["message"],
        )

        # Delete a Notification
        response = self.client.delete(
            reverse(
                viewname="detailed_crud_notification",
                args=[updated_notification["notification"]["id"]],
            ),
        )
        self.assertEqual(response.status_code, status.accepted)

        # Checking that the notification is soft deleted
        response = self.client.get(
            reverse(
                viewname="detailed_crud_notification",
                args=[updated_notification["notification"]["id"]],
            ),
        )
        deleted_notification = json.loads(response.content)
        self.assertEqual(deleted_notification["notification"]["deleted"], True)


class NotificationSenderTest(TestCase):
    """
    Test cases for the notification sending to different clients, depending on
    their preferences.
    """
    def setUp(self):
        """Creation of the clients with their respective notification
        preferences, and the base notification to send.
        """
        self.client = ServerClient()

        client = Client(
            name="test client 1",
            email="test1@test.com",
            cellphone="number client 1",
        )
        client.save()
        client_notification_preferences = NotificationPreferences.objects.get(
                client_id=client.id
        )
        client_notification_preferences.email = True
        client_notification_preferences.save()

        client = Client(
            name="test client 2",
            email="test2@test.com",
            cellphone="number client 2",
        )
        client.save()
        client_notification_preferences = NotificationPreferences.objects.get(
                client_id=client.id
        )
        client_notification_preferences.sms = True
        client_notification_preferences.save()

        client = Client(
            name="test client 3",
            email="test3@test.com",
            cellphone="number client 3",
        )
        client.save()
        client_notification_preferences = NotificationPreferences.objects.get(
                client_id=client.id
        )
        client_notification_preferences.email = True
        client_notification_preferences.sms = True
        client_notification_preferences.save()

        client = Client(
            name="test client 4",
            email="test4@test.com",
            cellphone="number client 4",
        )
        client.save()

        notification = Notifications(
            message="Test message to send"
        )
        notification.save()
        return

    def test_send_notifications(self):
        """
        Test flow for the sending of a notification to different clients.
        """
        response = self.client.get(
            reverse(viewname="notifications_sender"),
        )
        if response.status_code == status.ok:
            for chunk in response.streaming_content:
                print(json.loads(chunk))
