import boto3

client = boto3.client('s3')


def create_bucket(bucket_name: str, aws_region: str, acl: str):
    client.create_bucket(ACL=acl, Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': aws_region})
