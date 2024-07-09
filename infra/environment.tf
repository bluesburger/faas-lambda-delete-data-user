variable "region_provider_aws" {
  type = string
  description = "region aws"
  default = "us-east-1"
}

variable "function_name" {
  type = string
  description = "Nome da função lambda"
  default = "faas-delete-user-data"
}

variable "function_handler" {
  type = string
  description = "Handler da lambda"
  default = "lambda_function.lambda_handler"
}

variable "function_runtime" {
  type = string
  description = "Runtime da lambda"
  default = "python3.11"
}

variable "table_name_payment_dynamodb" {
  type = string
  description = "nome da tabela de pagamentos no dynamodb"
  default = "payment"
}

variable "secret_name_credentials_db" {
  type = string
  description = "nome do secret que armazena as credenciais"
  default = "/secret/RDSCredentials"
}