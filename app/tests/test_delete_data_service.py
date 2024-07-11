import unittest
from unittest.mock import patch, MagicMock

from aws_lambda_powertools.utilities.typing import LambdaContext

from src.delete_data_service import delete_data_user


class TestDeleteDataUser(unittest.TestCase):

    @patch('src.delete_data_service.delete_data_from_cognito')
    @patch('src.delete_data_service.delete_data_from_sqldb')
    @patch('src.delete_data_service.delete_data_from_dynamodb')
    def test_delete_data_user_success(self, mock_delete_data_from_dynamodb, mock_delete_data_from_sqldb,
                                      mock_delete_data_from_cognito):
        mock_delete_data_from_cognito.return_value = {'status': 'success'}
        mock_delete_data_from_sqldb.return_value = {'status': 'success'}
        mock_delete_data_from_dynamodb.return_value = {'status': 'success'}

        event = {'username': 'testuser', 'user_id': '123'}
        context = MagicMock(LambdaContext)
        result = delete_data_user(event, context)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['message'], 'Todos os dados do usuário foram excluídos')
        self.assertEqual(len(result['responses']), 3)
        for response in result['responses']:
            self.assertEqual(response['status'], 'success')

    @patch('src.delete_data_service.delete_data_from_cognito')
    @patch('src.delete_data_service.delete_data_from_sqldb')
    @patch('src.delete_data_service.delete_data_from_dynamodb')
    def test_delete_data_user_partial_error(self, mock_delete_data_from_dynamodb, mock_delete_data_from_sqldb,
                                            mock_delete_data_from_cognito):
        mock_delete_data_from_cognito.return_value = {'status': 'success'}
        mock_delete_data_from_sqldb.return_value = {'status': 'error'}
        mock_delete_data_from_dynamodb.return_value = {'status': 'success'}

        event = {'username': 'testuser', 'user_id': '123'}
        context = MagicMock(LambdaContext)
        result = delete_data_user(event, context)

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['message'], 'Alguns dados não puderam ser excluídos completamente')
        self.assertEqual(len(result['responses']), 3)
        self.assertEqual(result['responses'][0]['status'], 'success')
        self.assertEqual(result['responses'][1]['status'], 'error')
        self.assertEqual(result['responses'][2]['status'], 'success')
