from typing import Dict, List
import boto3
from mypy_boto3_glue import GlueClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

if settings.GLUE_ENDPOINT_URL:
    logger.info("Using local Glue client")
    glue: GlueClient = boto3.client("glue", endpoint_url=settings.GLUE_ENDPOINT_URL)
else:
    glue: GlueClient = boto3.client("glue")


def create_glue_crawler(crawler_name: str, prefix: str):
    """
    Check if databse exists, if not create one, then creates a Glue Crawler.
    Args:
        crawler_name (str): The name of the Glue Crawler.
    Returns:
        dict: The response from the Glue Crawler creation.
    Raises:
        Exception: If the Glue Crawler creation fails.
    """
    try:
        # split
        # Check if the database exists
        database_name = settings.GLUE_CATALOG_DATABASE
        try:
            glue.get_database(Name=database_name)
        except glue.exceptions.EntityNotFoundException:
            glue.create_database(DatabaseInput={"Name": database_name})

        # Create the Glue Crawler
        s3 = boto3.resource("s3", endpoint_url=settings.S3_ENDPOINT_URL)
        target = f"s3://{settings.S3_BUCKET_NAME}/preview/{prefix}"
        database_name = settings.GLUE_CATALOG_DATABASE
        crawler = glue.create_crawler(
            DatabaseName=database_name,
            Name=crawler_name,
            Role=settings.GLUE_CRAWLER_ROLE_ARN,
            Targets={"S3Targets": [{"Path": target}]},
        )
        return crawler
    except Exception as e:
        raise e


def submit_crawler_job(file_key:str) -> str:
    """
    1. check if there is a glue crawler existed based on the crawler name, if not create one against s3 bucket data folder
    2. check if the crawler is in pending, running or cancelling state, if so return the running id, otherwise start the crawler
    Submits a Glue Crawler job.
    Args:
        crawler_name (str): The name of the Glue Crawler.

    Returns:
        str: The job run ID of the submitted Glue Crawler job.
    """
    # split fileKey by /, and the prefix
    prefix = file_key.split("/")[1]
    # Check if the crawler exists
    crawler_name = f"{settings.GLUE_CRAWLER_NAME}_{prefix}"
    try:
        crawler = glue.get_crawler(Name=crawler_name)
    except glue.exceptions.EntityNotFoundException:
        create_glue_crawler(crawler_name, prefix)

    response = glue.start_crawler(Name=crawler_name)
    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception("Failed to start Glue Crawler job.")
    return crawler_name


def get_crawler_job_status(crawler_name: str) -> str:
    """
    Retrieves the status of a Glue Crawler job.
    Args:
        crawler_name (str): The name of the Glue Crawler.

    Returns:
        str: The status of the Glue Crawler job.
    """
    crawler = glue.get_crawler(Name=crawler_name)
    return crawler["Crawler"]["State"]


def get_crawler_job_metrics(crawler_name: str) -> dict:
    """
    Retrieves the metrics of a Glue Crawler job.
    Args:
        crawler_name (str): The name of the Glue Crawler.

    Returns:
        dict: The metrics of the Glue Crawler job.
    """
    crawler = glue.get_crawler_metrics(CrawlerNameList=[crawler_name])
    return crawler["CrawlerMetricsList"][0]["Metrics"]


def get_crawled_tables_from_database() -> List[Dict]:
    """
    Get a list of crawled tables from a database in AWS Glue.

    Args:
        database_name (str): The name of the database.

    Returns:
        List[Dict]: A list of dictionaries containing table details.
    """
    try:
        database_name = settings.GLUE_CATALOG_DATABASE
        tables = []
        response = glue.get_tables(DatabaseName=database_name)
        return response["TableList"]
    except glue.exceptions.EntityNotFoundException:
        print(f"Database '{database_name}' not found.")
        return []
    except Exception as e:
        print(f"Error getting tables from database '{database_name}': {e}")
        return []
