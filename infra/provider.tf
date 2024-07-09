provider "aws" {
  region = var.region_provider_aws
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "bb-ordering-system-production"
    key    = "lambda-delete-user-data/terraform.tfstate"
    region = "us-east-1"
  }
}