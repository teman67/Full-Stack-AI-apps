# AWS Infrastructure for Full-Stack AI Apps

# VPC and Networking
resource "aws_vpc" "ai_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-vpc"
  })
}

resource "aws_subnet" "ai_subnet_public" {
  count             = 2
  vpc_id            = aws_vpc.ai_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-subnet-public-${count.index + 1}"
    Type = "Public"
  })
}

resource "aws_subnet" "ai_subnet_private" {
  count             = 2
  vpc_id            = aws_vpc.ai_vpc.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-subnet-private-${count.index + 1}"
    Type = "Private"
  })
}

resource "aws_internet_gateway" "ai_igw" {
  vpc_id = aws_vpc.ai_vpc.id

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-igw"
  })
}

# Security Groups
resource "aws_security_group" "ai_api_sg" {
  name_prefix = "${var.project_name}-api-"
  vpc_id      = aws_vpc.ai_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-api-sg"
  })
}

# IAM Roles for Bedrock and SageMaker
resource "aws_iam_role" "bedrock_execution_role" {
  name = "${var.project_name}-${var.environment}-bedrock-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = ["bedrock.amazonaws.com", "lambda.amazonaws.com"]
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "bedrock_policy" {
  name = "${var.project_name}-${var.environment}-bedrock-policy"
  role = aws_iam_role.bedrock_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:CreateAgent",
          "bedrock:GetAgent",
          "bedrock:UpdateAgent",
          "bedrock:DeleteAgent"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role" "sagemaker_execution_role" {
  name = "${var.project_name}-${var.environment}-sagemaker-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_execution_role_policy" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

# S3 Bucket for ML artifacts
resource "aws_s3_bucket" "ml_artifacts" {
  bucket = "${var.project_name}-${var.environment}-ml-artifacts-${random_id.bucket_suffix.hex}"
}

resource "aws_s3_bucket_versioning" "ml_artifacts_versioning" {
  bucket = aws_s3_bucket.ml_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_encryption" "ml_artifacts_encryption" {
  bucket = aws_s3_bucket.ml_artifacts.id

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

# Lambda function for AI processing
resource "aws_lambda_function" "ai_processor" {
  filename         = "ai_processor.zip"
  function_name    = "${var.project_name}-${var.environment}-ai-processor"
  role            = aws_iam_role.lambda_execution_role.arn
  handler         = "index.handler"
  runtime         = "python3.9"
  timeout         = 300

  environment {
    variables = {
      BEDROCK_REGION = var.aws_region
      S3_BUCKET     = aws_s3_bucket.ml_artifacts.bucket
    }
  }

  tags = local.common_tags
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# ECS Cluster for containerized AI services
resource "aws_ecs_cluster" "ai_cluster" {
  name = "${var.project_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = local.common_tags
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "ai_logs" {
  name              = "/aws/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 30

  tags = local.common_tags
}

# Application Load Balancer
resource "aws_lb" "ai_alb" {
  name               = "${var.project_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ai_api_sg.id]
  subnets           = aws_subnet.ai_subnet_public[*].id

  enable_deletion_protection = false

  tags = local.common_tags
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

# Random ID for unique resource naming
resource "random_id" "bucket_suffix" {
  byte_length = 8
}

# Outputs
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.ai_vpc.id
}

output "bedrock_role_arn" {
  description = "Bedrock execution role ARN"
  value       = aws_iam_role.bedrock_execution_role.arn
}

output "sagemaker_role_arn" {
  description = "SageMaker execution role ARN"
  value       = aws_iam_role.sagemaker_execution_role.arn
}

output "ml_artifacts_bucket" {
  description = "ML artifacts S3 bucket"
  value       = aws_s3_bucket.ml_artifacts.bucket
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.ai_cluster.name
}

output "load_balancer_dns" {
  description = "Load balancer DNS name"
  value       = aws_lb.ai_alb.dns_name
}