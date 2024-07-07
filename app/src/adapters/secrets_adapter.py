import json
import os
import boto3
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()

region_name = os.getenv('REGION_AWS')


def recuperar_segredo(secret_name: str) -> dict:
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response['SecretString']

        logger.info("Segredo recuperado com sucesso.")
        return json.loads(secret_string)
    except Exception as e:
        logger.error(f"Falha ao recuperar segredo: {e}")
        raise e
