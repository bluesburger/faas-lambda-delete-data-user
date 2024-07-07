import os

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

logger = Logger()

USER_POOL_ID = os.getenv('USER_POOL_ID')
cognito_client = boto3.client('cognito-idp')


def delete_data_from_cognito(username):
    logger.info(f'Deleting user: {username} from cognito user pool: {USER_POOL_ID}')
    try:
        cognito_client.admin_delete_user(
            UserPoolId=USER_POOL_ID,
            Username=username
        )
        logger.info(f'User excluded with success: {username} from cognito user pool: {USER_POOL_ID}')
    except ClientError as e:
        logger.error(f'Error deleting: {e.response["Error"]["Message"]}')
        return {'status': {e.response["Error"]["Message"]['error_code']}, 'message': str(e)}
    except cognito_client.exceptions.UserNotFoundException as e:
        logger.error(f'Error deleting: {e.response["Error"]["Message"]}')
        return {'status': 404, 'message': str(e)}
