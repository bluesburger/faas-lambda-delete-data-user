import json
import os
import sys

import pymysql as mysql
from aws_lambda_powertools import Logger

from src.adapters.secrets_adapter import recuperar_segredo
from src.adapters.utils.queries import DELETE_USER_QUERY

logger = Logger()

secret_name = os.getenv('SECRET_NAME')


def delete_data_from_sqldb(user_id):
    credenciais_db = recuperar_segredo(secret_name)

    try:
        with open_connection_with_db(credenciais_db) as db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute(DELETE_USER_QUERY, user_id)
                db_connection.commit()
    except mysql.MySQLError as e:
        logger.error(f"MySQL error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error deleting user data')
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Unexpected error deleting user data')
        }


def open_connection_with_db(credenciais_db):
    try:
        return mysql.connect(
            host=credenciais_db['host_db'],
            user=credenciais_db['user_db'],
            password=credenciais_db['password_db'],
            database=credenciais_db['database_db'],
            connect_timeout=5
        )
    except mysql.MySQLError as e:
        logger.error(f"ERROR: Unexpected error: Could not connect to MySQL instance. {e}")
        sys.exit(1)
