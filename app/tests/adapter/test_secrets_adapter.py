import json
import os
import unittest
from unittest.mock import patch, MagicMock

from botocore.exceptions import ClientError

from src.adapters.secrets_adapter import recuperar_segredo


class TestSecretAdapter(unittest.TestCase):

    @patch.dict(os.environ, {"REGION_AWS": "region_fake"})
    @patch('src.adapters.secrets_adapter.boto3.client')
    def test_recuperar_segredo_sucesso(self, mock_secret_client):
        mock_client = MagicMock()
        mock_client.get_secret_value.return_value = {'SecretString': json.dumps({'key': 'value'})}
        mock_secret_client.return_value = mock_client

        resultado = recuperar_segredo('my_secret')

        self.assertEqual(resultado, {'key': 'value'})
        mock_client.get_secret_value.assert_called_once_with(
            SecretId='my_secret'
        )

    @patch.dict(os.environ, {"REGION_AWS": "region_fake"})
    @patch('src.adapters.secrets_adapter.boto3.client')
    def test_recuperar_segredo_falha_client_error(self, mock_secret_client):
        mock_client = MagicMock()
        error_response = {'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}}
        mock_client.get_secret_value.side_effect = ClientError(
            error_response=error_response,
            operation_name='GetSecretValue'
        )
        mock_secret_client.return_value = mock_client

        with self.assertRaises(ClientError):
            recuperar_segredo('my_secret')

    @patch.dict(os.environ, {"REGION_AWS": "region_fake"})
    @patch('src.adapters.secrets_adapter.boto3.client')
    def test_recuperar_segredo_falha_generica(self, mock_secret_client):
        mock_client = MagicMock()
        mock_client.get_secret_value.side_effect = Exception('Erro genérico')
        mock_secret_client.return_value = mock_client

        with self.assertRaises(Exception):
            recuperar_segredo('my_secret')
