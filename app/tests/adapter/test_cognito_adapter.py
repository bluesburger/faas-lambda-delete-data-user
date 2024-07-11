import os
import unittest
from unittest.mock import patch

from botocore.exceptions import ClientError

from src.adapters.cognito_adapter import delete_data_from_cognito


class TestDeleteDataFromCognito(unittest.TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.user_pool_id = 'test_user_pool_id'

    @patch.dict(os.environ, {"USER_POOL_ID": "test_user_pool_id"})
    @patch('src.adapters.cognito_adapter.cognito_client')
    def test_delete_user_success(self, mock_cognito_client):
        mock_cognito_client.admin_delete_user.return_value = None

        response = delete_data_from_cognito(self.username)

        self.assertIsNone(response)
        mock_cognito_client.admin_delete_user.assert_called_once_with(
            UserPoolId=self.user_pool_id,
            Username=self.username
        )

    @patch.dict(os.environ, {"USER_POOL_ID": "test_user_pool_id"})
    @patch('src.adapters.cognito_adapter.cognito_client')
    def test_delete_user_client_error(self, mock_cognito_client):
        error_response = {
            'Error': {
                'Message': 'An error occurred',
                'Code': 'ClientError'
            }
        }
        mock_cognito_client.admin_delete_user.side_effect = ClientError(
            error_response, 'AdminDeleteUser'
        )

        response = delete_data_from_cognito(self.username)

        self.assertEqual(response['status'], {'ClientError'})
        self.assertEqual(response['message'],
                         "An error occurred (ClientError) when calling the AdminDeleteUser operation:"
                         " An error occurred")


