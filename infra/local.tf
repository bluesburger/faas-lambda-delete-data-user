locals {
  environment_variables = {
    USER_POOL_ID        = "us-east-1_F5BiZuEcH"
    DYNAMODB_TABLE_NAME = var.table_name_payment_dynamodb
    REGION_AWS          = var.region_provider_aws
    SECRET_NAME         = var.secret_name_credentials_db
  }
}