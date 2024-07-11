resource "aws_cloudwatch_log_group" "lambda_create_logs" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 1
}