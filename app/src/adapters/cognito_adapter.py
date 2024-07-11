import os

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger()

cognito_client = boto3.client('cognito-idp')


def delete_data_from_cognito(username):
    user_pool_id = os.getenv('USER_POOL_ID')

    logger.info(f'Deleting user: {username} from cognito user pool: {user_pool_id}')
    try:
        cognito_client.admin_delete_user(
            UserPoolId=user_pool_id,
            Username=username
        )
        logger.info(f'User excluded with success: {username} from cognito user pool: {user_pool_id}')
    except ClientError as e:
        logger.error(f'Error deleting: {e.response["Error"]["Message"]}')
        return {'status': {e.response["Error"]["Code"]}, 'message': str(e)}

