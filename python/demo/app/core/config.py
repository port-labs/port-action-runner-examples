from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "demo"
    PORT_API_URL: str = "https://demo.getport.io:3000/v1"
    PORT_S3_BUCKET_BLUEPRINT: str = "S3Bucket"
    PORT_CLIENT_ID: str = '60EsooJtOqimlekxrNh7nfr2iOgTcyLZ'
    PORT_CLIENT_SECRET: str = 'Tho9hoyjQYomojauapUM3XCC5vMkVO5SWUAxWWGPAb4rQaPexG3jhQPB5WKUIoDx'


    class Config:
        case_sensitive = True


settings = Settings()
