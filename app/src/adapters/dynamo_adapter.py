import os

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger()

dynamodb_client = boto3.client('dynamodb')
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')


def delete_data_from_dynamodb(user_id):
    logger.info(f'Deleting data user: {user_id} in dynamodb: {DYNAMODB_TABLE_NAME}')

    try:
        dynamodb_client.delete_item(
            TableName=DYNAMODB_TABLE_NAME,
            Key={
                'user_id': {'S': user_id}
            }
        )
        logger.info(f'Data excluded with success: {user_id} in dynamodb: {DYNAMODB_TABLE_NAME}')
    except ClientError as e:
        logger.error(f'Error deleting: {e.response["Error"]["Message"]}')
        return {'status': 'error', 'message': str(e)}
