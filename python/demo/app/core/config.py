from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "demo"
    PORT_API_URL: str = "http://localhost:3000/v1"
    PORT_CLIENT_ID: str = "60EsooJtOqimlekxrNh7nfr2iOgTcyLZ"
    PORT_CLIENT_SECRET: str = "WWyIqRypzIVtw3eDDmyxPuoqdHM4pV8SHUXq5qHkeLwZguRGuirKAR9NPZ7Jl2ml"

    # "https://demo.getport.io:3000/v1"
    
    PORT_S3_BUCKET_BLUEPRINT: str = "S3Bucket"

    class Config:
        case_sensitive = True


settings = Settings()
