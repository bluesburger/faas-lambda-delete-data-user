resource "aws_lambda_function" "lambda_faas_delete_user_data" {
  function_name = var.function_name
  handler       = var.function_handler
  runtime       = var.function_runtime
  role          = aws_iam_role.lambda_role.arn
  filename      = "${path.root}/../deploy/lambda_function.zip"
  environment {
    variables = local.environment_variables
  }
}