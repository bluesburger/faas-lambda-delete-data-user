import os
import unittest
from unittest.mock import patch

from botocore.exceptions import ClientError

from src.adapters.dynamo_adapter import delete_data_from_dynamodb


class TestDeleteDataFromDynamoDB(unittest.TestCase):

    @patch.dict(os.environ, {"DYNAMODB_TABLE_NAME": "test_table"})
    @patch('src.adapters.dynamo_adapter.dynamodb_client')
    def test_delete_item_success(self, mock_dynamodb_client):
        mock_dynamodb_client.delete_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        response = delete_data_from_dynamodb('user123')

        self.assertIsNone(response)
        mock_dynamodb_client.delete_item.assert_called_once_with(
            TableName='test_table',
            Key={'user_id': {'S': 'user123'}}
        )

    @patch.dict(os.environ, {"DYNAMODB_TABLE_NAME": "test_table"})
    @patch('src.adapters.dynamo_adapter.dynamodb_client')
    def test_delete_item_client_error(self, mock_dynamodb_client):
        error_response = {'Error': {'Message': 'Item not found', 'Code': 'ConditionalCheckFailedException'}}
        mock_dynamodb_client.delete_item.side_effect = ClientError(error_response, 'DeleteItem')

        response = delete_data_from_dynamodb('user456')

        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['message'], 'Item not found')
