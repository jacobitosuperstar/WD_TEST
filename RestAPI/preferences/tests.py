import json
from django.test import (
    TestCase,
    Client as ServerClient,
)
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status


class ClientsPreferencesWorkflowTest(TestCase):
    """
    Set of test cases for listing, getting, creating, updating and deleting
    clients.
    """
    def setUp(self):
        self.client = ServerClient()
        return


    def test_get_update_preferences(self):
        """
        Create a client and get their base preferences. After that, update
        the preferences of said client.
        """
        # Create a client
        msg = {
            "name": "test name 1",
            "email": "test1@test.com",
            "cellphone": "1234567890",

        }
        response = self.client.post(
            reverse(viewname="create_client"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.created)
        created_client_info = json.loads(response.content)

        # get an specific client notification preferences
        response = self.client.get(
            reverse(
                viewname="detailed_preferences",
                args=[created_client_info["client"]["id"]],
            ),
        )
        self.assertEqual(response.status_code, status.accepted)

        # update an specific client notification preferences
        msg = {
            "email": True,
            "sms": True,
        }
        response = self.client.post(
            reverse(
                viewname="detailed_preferences",
                args=[created_client_info["client"]["id"]],
            ),
            data=msg,
        )
        new_preferences = json.loads(response.content)
        self.assertEqual(response.status_code, status.accepted)
        self.assertEqual(
            new_preferences["notification_preferences"]["email"],
            msg["email"]
        )
        self.assertEqual(
            new_preferences["notification_preferences"]["sms"],
            msg["sms"]
        )
