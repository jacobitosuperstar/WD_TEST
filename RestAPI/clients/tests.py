import json
from django.test import (
    TestCase,
    Client as ServerClient,
)
from django.urls import reverse
from base.http_status_codes import HTTP_STATUS as status


class ClientsWorkflowTest(TestCase):
    """
    Set of test cases for listing, getting, creating, updating and deleting
    clients.
    """
    def setUp(self):
        self.client = ServerClient()
        return


    def test_create_get_clients(self):
        """
        Test flow for the creation of several clients and checking that
        all the information regarding them is actually recorded on the DB.
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

        msg = {
            "name": "test name 2",
            "email": "test2@test.com",
            "cellphone": "1234567890",

        }
        response = self.client.post(
            reverse(viewname="create_client"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.created)
        created_client_info_2 = json.loads(response.content)

        # listing all the clients
        response = self.client.get(
            reverse(viewname="clients_list")
        )
        self.assertEqual(response.status_code, status.ok)

        # get an specific client
        response = self.client.get(
            reverse(
                viewname="detailed_client",
                args=[created_client_info_2["client"]["id"]],
            ),
        )
        self.assertEqual(response.status_code, status.accepted)
        specific_client = json.loads(response.content)
        self.assertEqual(
            created_client_info_2["client"]["id"],
            specific_client["client"]["id"]
        )


    def test_create_update_delete_client(self):
        """
        Test flow for the creation, update and soft deletion of a client.
        """
        # Create a client
        msg = {
            "name": "test name",
            "email": "test@test.com",
            "cellphone": "1234567890",

        }
        response = self.client.post(
            reverse(viewname="create_client"),
            data=msg,
        )
        self.assertEqual(response.status_code, status.created)
        created_client_info = json.loads(response.content)

        # Update a client

        msg = {"cellphone": "0987654321"}

        response = self.client.post(
            reverse(
                viewname="update_client",
                args=[created_client_info["client"]["id"]],
            ),
            data=msg,
        )
        self.assertEqual(response.status_code, status.accepted)

        # Delete a client
        response = self.client.delete(
            reverse(
                viewname="delete_client",
                args=[created_client_info["client"]["id"]],
            ),
        )
        self.assertEqual(response.status_code, status.accepted)

        # Checking that the client is soft deleted
        response = self.client.get(
            reverse(
                viewname="detailed_client",
                args=[created_client_info["client"]["id"]],
            ),
            data=msg,
        )
        deleted_client_info = json.loads(response.content)
        self.assertEqual(deleted_client_info["client"]["deleted"], True)
