from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "s3_bucket_creation/github_action"

    PORT_API_URL: str = "https://api.getport.io/v1"
    PORT_CLIENT_ID: str
    PORT_CLIENT_SECRET: str

    GH_DEFAULT_BRANCH: str = "main"
    GH_ORGANIZATION: str
    GH_REPOSITORY: str
    GH_WORKFLOW_FILE_NAME: str
    GH_ACCESS_TOKEN: str

    class Config:
        case_sensitive = True


settings = Settings()
