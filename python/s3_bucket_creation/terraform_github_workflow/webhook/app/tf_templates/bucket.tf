terraform {
  required_providers {
    port-labs = {
      source  = "port-labs/port-labs"
      version = "~> 0.4.0"
    }
  }
}
provider "port-labs" {}

provider "aws" {
  alias  = "bucket_region"
  region = "{{ region }}"
}

resource "aws_s3_bucket" "example" {
  provider = aws.bucket_region
  bucket   = "{{ bucket_name }}"
}

resource "aws_s3_bucket_acl" "example_bucket_acl" {
  bucket = aws_s3_bucket.example.id
  acl    = "{{ acl }}"
}

resource "port-labs_entity" "bucket_port_entity" {
  identifier = "{{ bucket_name }}"
  title      = "{{ bucket_name }}"
  blueprint  = "S3Bucket"
  properties {
    name  = "acl"
    value = "{{ acl }}"
  }
  properties {
    name  = "awsRegion"
    value = "{{ region }}"
  }
  properties {
    name  = "createdDate"
    value = timestamp()
  }
  properties {
    name  = "S3Link"
    value = "https://s3.console.aws.amazon.com/s3/buckets/{{ bucket_name }}"
  }
  depends_on = [aws_s3_bucket.example, aws_s3_bucket_acl.example_bucket_acl]
}
