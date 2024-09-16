from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Simple Data Analytics API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    S3_BUCKET_NAME:str = "warrewei-q-dev-demo"
    # Add other configuration variables here

    class Config:
        env_file = ".env"

settings = Settings()
