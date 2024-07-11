import unittest
from unittest.mock import patch, MagicMock

import pymysql

from src.adapters.rds_adapter import delete_data_from_sqldb, open_connection_with_db
from src.adapters.utils.queries import DELETE_USER_QUERY


class TestDeleteDataFromSQLDB(unittest.TestCase):

    @patch.dict('src.adapters.rds_adapter.os.environ', {'SECRET_NAME': 'test_secret_name'})
    @patch('src.adapters.rds_adapter.recuperar_segredo')
    @patch('src.adapters.rds_adapter.mysql.connect')
    def test_delete_data_success(self, mock_open_connection_with_db, mock_recuperar_segredo):
        mock_recuperar_segredo.return_value = {
            'host_db': 'mock_host',
            'user_db': 'mock_user',
            'password_db': 'mock_password',
            'database_db': 'mock_database'
        }
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_open_connection_with_db.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        response = delete_data_from_sqldb('user123')

        mock_cursor.execute.assert_called_once_with(DELETE_USER_QUERY, ('user123',))
        mock_connection.commit.assert_called_once()
        self.assertIsNone(response)

    @patch.dict('src.adapters.rds_adapter.os.environ', {'SECRET_NAME': 'test_secret_name'})
    @patch('src.adapters.secrets_adapter.recuperar_segredo')
    @patch('src.adapters.rds_adapter.mysql.connect')
    def test_connection_error(self, mock_mysql_connect, mock_recuperar_segredo):
        mock_recuperar_segredo.return_value = {
            'host_db': 'mock_host',
            'user_db': 'mock_user',
            'password_db': 'mock_password',
            'database_db': 'mock_database'
        }
        mock_mysql_connect.side_effect = pymysql.MySQLError("Connection error")

        with self.assertRaises(SystemExit):
            open_connection_with_db(mock_recuperar_segredo.return_value)

    @patch.dict('src.adapters.rds_adapter.os.environ', {'SECRET_NAME': 'test_secret_name'})
    @patch('src.adapters.rds_adapter.recuperar_segredo')
    @patch('src.adapters.rds_adapter.mysql.connect')
    def test_delete_data_mysql_error(self, mock_open_connection_with_db, mock_recuperar_segredo):
        mock_recuperar_segredo.return_value = {
            'host_db': 'mock_host',
            'user_db': 'mock_user',
            'password_db': 'mock_password',
            'database_db': 'mock_database'
        }
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_open_connection_with_db.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = pymysql.MySQLError("Query error")

        response = delete_data_from_sqldb('user123')

        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error deleting user data', response['body'])

    @patch.dict('src.adapters.rds_adapter.os.environ', {'SECRET_NAME': 'test_secret_name'})
    @patch('src.adapters.rds_adapter.recuperar_segredo')
    @patch('src.adapters.rds_adapter.mysql.connect')
    def test_delete_data_unexpected_error(self, mock_open_connection_with_db, mock_recuperar_segredo):
        mock_recuperar_segredo.return_value = {
            'host_db': 'mock_host',
            'user_db': 'mock_user',
            'password_db': 'mock_password',
            'database_db': 'mock_database'
        }
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_open_connection_with_db.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Unexpected error")

        response = delete_data_from_sqldb('user123')

        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Unexpected error deleting user data', response['body'])


