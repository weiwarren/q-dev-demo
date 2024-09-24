from pydantic import BaseSettings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Data Analytics API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    AWS_REGION: str = "ap-southeast-2"
    ALLOWED_HOSTS: list[str] = ["*"]
    ENVIRONMENT: str = "local"
    IS_LOCAL: bool = ENVIRONMENT == "local"
    S3_PREVIEW_PREFIX = "preview"
    NUM_PREVIEW_ROWS = 100

    S3_BUCKET_NAME: str = "local"

    GLUE_CRAWLER_ROLE_ARN = "arn:"
    GLUE_CRAWLER_NAME = "simple_data_analytics_crawler"
    GLUE_CATALOG_DATABASE = "simple_data_analytics_database"

    ATHENA_OUTPUT_LOCATION = "aws-athena-query-results-000000000000-ap-southeast-2"
    
    @property
    def S3_ENDPOINT_URL(self) -> str:
        if self.ENVIRONMENT == "local":
            return "http://localhost:4566"
        return None
    
    @property
    def GLUE_ENDPOINT_URL(self) -> str:
        if self.ENVIRONMENT == "local":
            return "http://localhost:4566"
        return None

    @property
    def ATHENA_ENDPOINT_URL(self) -> str:
        if self.ENVIRONMENT == "local":
            return "http://localhost:4566"
        return None
    
    @property
    def IS_LOCAL(self) -> bool:
        return self.ENVIRONMENT == "local"

    class Config:
        env_file_encoding = "utf-8"


settings = Settings()
