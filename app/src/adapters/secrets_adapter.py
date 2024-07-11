import json
import os

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger()


def recuperar_segredo(secret_name: str) -> dict:
    region_name = os.getenv('REGION_AWS')
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response['SecretString']

        logger.info("Segredo recuperado com sucesso.")
        return json.loads(secret_string)
    except ClientError as e:
        logger.error(f"Erro do cliente ao recuperar segredo: {e.response['Error']['Message']}")
        raise e
    except Exception as e:
        logger.error(f"Falha ao recuperar segredo: {e}")
        raise e
