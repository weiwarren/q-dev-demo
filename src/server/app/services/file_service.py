import os
import uuid
from typing import List, Any
from fastapi import UploadFile
from app.config import settings
import pandas as pd
import numpy as np
import boto3
from botocore import exceptions as botocore_exceptions
import logging

logger = logging.getLogger(__name__)

if settings.S3_ENDPOINT_URL:
    print("Using local S3 client")
    s3 = boto3.client("s3", endpoint_url=settings.S3_ENDPOINT_URL)
else:
    print("Using prod S3 client")
    s3 = boto3.client("s3")
large_number = 1e308  # Maximum float value in Python


class FileService:
    def list_buckets():
        """
        list buckets with name prefixed data
        """
        aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"
        aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        response = s3.list_buckets()
        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        return buckets


    async def upload_file(self, file: UploadFile) -> str:
        """
        Uploads a file to Amazon S3 bucket using boto3 with a unique file key.
        """

        file_key = f"{settings.S3_PREVIEW_PREFIX}/{str(uuid.uuid4())}/{file.filename}"
        file_content = await file.read()
        # Use boto3 to upload the file to S3 bucket
        try:
            s3.upload_fileobj(file.file, settings.S3_BUCKET_NAME, file_key)
            return file_key
        except botocore_exceptions.ClientError as e:
            print(f"Error uploading file to S3: {e}")
            raise e

    async def preview_file(self, file_key: str) -> dict:
        """
        Previews the first few rows of a CSV file.

        Args:
            file_key (str): The unique file key for the uploaded file.

        Returns:
            {headers: columns data, data: rows}
        """
        # Use boto3 to download the file from S3 bucket
        try:
            obj = s3.get_object(Bucket=settings.S3_BUCKET_NAME, Key=file_key)
            print("successfully got file")
            file_content = obj["Body"]
            nrows = settings.NUM_PREVIEW_ROWS

            # Read top 100 rows from csv

            data = pd.read_csv(
                file_content,
                nrows=nrows,
                dtype=object,
            )

            print("successfully read file")

            data = data.replace([np.inf, -np.inf], np.nan)
            data = data.fillna(method="ffill")

            # Convert data types for each column
            for col in data.columns:
                col_data = data[col].infer_objects()
                if col_data.dtypes == "int64":
                    data[col] = col_data.astype("Int64")
                elif col_data.dtypes == "float64":
                    data[col] = col_data.astype("float64").apply(
                        lambda x: x if x == x else None
                    )

            headers = data.columns.tolist()
            data = [list(row) for row in data.values]
            print("successfully converted data")
            return {"headers": headers, "data": data}
        except botocore_exceptions.ClientError as e:
            logger.error(f"Error downloading file from S3: {e}")
            raise e
