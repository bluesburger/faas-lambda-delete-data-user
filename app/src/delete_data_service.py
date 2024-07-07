from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.adapters.cognito_adapter import delete_data_from_cognito
from src.adapters.dynamo_adapter import delete_data_from_dynamodb
from src.adapters.rds_adapter import delete_data_from_sqldb

logger = Logger(service="delete_data_user")


@logger.inject_lambda_context
def delete_data_user(event, context: LambdaContext):
    responses = []

    cognito_result = delete_data_from_cognito(event['username'])
    responses.append(cognito_result)

    orders_result = delete_data_from_sqldb(event['user_id'])
    responses.append(orders_result)

    payments_result = delete_data_from_dynamodb(event['user_id'])
    responses.append(payments_result)

    status = 'success'
    message = 'Todos os dados do usuário foram excluídos'
    for response in responses:
        if response['status'] == 'error':
            status = 'error'
            message = 'Alguns dados não puderam ser excluídos completamente'

    return {
        'status': status,
        'message': message,
        'responses': responses
    }
