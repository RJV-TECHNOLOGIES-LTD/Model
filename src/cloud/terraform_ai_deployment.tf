provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "ai_model_storage" {
  bucket = "ai-execution-models-bucket"
  acl    = "private"
}

output "bucket_name" {
  value = aws_s3_bucket.ai_model_storage.id
}
