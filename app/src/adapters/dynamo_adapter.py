import os

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger()

dynamodb_client = boto3.client('dynamodb')


def delete_data_from_dynamodb(user_id):
    dynamodb_table_name = os.getenv('DYNAMODB_TABLE_NAME')

    logger.info(f'Deleting data user: {user_id} in dynamodb: {dynamodb_table_name}')
    try:
        dynamodb_client.delete_item(
            TableName=dynamodb_table_name,
            Key={
                'user_id': {'S': user_id}
            }
        )
        logger.info(f'Data excluded with success: {user_id} in dynamodb: {dynamodb_table_name}')
    except ClientError as e:
        logger.error(f'Error deleting: {e.response["Error"]["Message"]}')
        return {'status': 'error', 'message': str(e.response["Error"]["Message"])}
