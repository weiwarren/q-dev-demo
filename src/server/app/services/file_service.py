from fastapi import UploadFile
from app.schemas import UploadResponse, PreviewResponse, SubmitResponse
import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException
from app.schemas import UploadResponse
from app.core.config import settings
import uuid


async def upload_file(file: UploadFile) -> UploadResponse:
    """
    Upload a file to Amazon S3.

    Args:
        file (UploadFile): The file to upload.

    Returns:
        UploadResponse: The response containing the file ID and a success message.

    Raises:
        HTTPException: If there's an error during file upload.
    """
    # raise exception if file name is not set
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is required")
    try:
        # Generate a unique file ID
        file_id = str(uuid.uuid4())

        # Create an S3 client
        s3 = boto3.client("s3")

        file_extension = file.filename.split(".")[-1] if file.filename else None

        # Generate a unique S3 object key
        s3_key = f"{file_id}.{file_extension}" if file_extension else file_id

        # Upload the file to S3

        s3.upload_fileobj(file.file, settings.S3_BUCKET_NAME, s3_key)

        res = UploadResponse(
            file_id=file_id, message="File uploaded successfully to S3"
        )
        return res

    except ClientError as e:
        # Handle S3-specific errors
        error_message = e.response["Error"]["Message"]
        raise HTTPException(
            status_code=500, detail=f"S3 upload failed: {error_message}"
        )
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


async def preview_file(file_id: str) -> PreviewResponse:
    """
    Preview the top 100 rows of a file.

    Args:
        file_id (str): The ID of the file to preview.

    Returns:
        PreviewResponse: The response containing the preview data and columns.
    """
    # Implement file preview logic here
    pass


async def submit_file(file_id: str) -> SubmitResponse:
    """
    Submit a file to S3 and trigger a Glue crawler job.

    Args:
        file_id (str): The ID of the file to submit.

    Returns:
        SubmitResponse: The response containing the job ID and a success message.
    """
    # Implement file submission logic here
    pass
