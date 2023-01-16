from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"

    PORT_API_URL: str = "http://localhost:3000/v1"
    PORT_S3_BUCKET_BLUEPRINT: str = "S3Bucket"
    PORT_CLIENT_ID: str = ''
    PORT_CLIENT_SECRET: str = ''

    class Config:
        case_sensitive = True


settings = Settings()
