from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "demo"
    PORT_API_URL: str = "https://demo.getport.io:3000/v1"
    PORT_S3_BUCKET_BLUEPRINT: str = "S3Bucket"

    class Config:
        case_sensitive = True


settings = Settings()
