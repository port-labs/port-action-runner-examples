from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "s3_bucket_creation/aws_sdk"

    PORT_API_URL: str = "https://api.getport.io/v1"
    PORT_S3_BUCKET_BLUEPRINT: str = "S3Bucket"
    PORT_CLIENT_ID: str
    PORT_CLIENT_SECRET: str

    AWS_S3_BUCKET_LINK: str = "https://s3.console.aws.amazon.com/s3/buckets/{bucket_name}"

    class Config:
        case_sensitive = True


settings = Settings()
