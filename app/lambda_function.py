from aws_lambda_powertools import Logger

from src.delete_data_service import delete_data_user

logger = Logger()


def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    delete_data_user(event, context)
    logger.info(f"End of event: {event}")
