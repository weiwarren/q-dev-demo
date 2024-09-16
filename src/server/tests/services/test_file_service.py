import pytest
from fastapi import UploadFile, HTTPException
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError
from app.services.file_service import upload_file
from app.schemas import UploadResponse

s3_bucket_name = "warrewei-q-dev-demo"


@pytest.fixture
def mock_s3_client():
    with patch("boto3.client") as mock_client:
        yield mock_client.return_value


@pytest.fixture
def mock_uuid():
    with patch("uuid.uuid4") as mock_uuid:
        mock_uuid.return_value = "test-uuid"
        yield mock_uuid


@pytest.mark.asyncio
async def test_upload_file_success(mock_s3_client, mock_uuid):
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.csv"
    mock_file.file = MagicMock()

    # Act
    result = await upload_file(mock_file)

    # Assert
    assert isinstance(result, UploadResponse)
    assert result.file_id == "test-uuid"
    assert result.message == "File uploaded successfully to S3"
    mock_s3_client.upload_fileobj.assert_called_once_with(
        mock_file.file, s3_bucket_name, "test-uuid.csv"
    )


@pytest.mark.asyncio
async def test_upload_file_no_extension(mock_s3_client, mock_uuid):
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test"
    mock_file.file = MagicMock()

    # Act
    result = await upload_file(mock_file)

    # Assert
    assert isinstance(result, UploadResponse)
    assert result.file_id == "test-uuid"
    assert result.message == "File uploaded successfully to S3"
    mock_s3_client.upload_fileobj.assert_called_once_with(
        mock_file.file, s3_bucket_name, "test-uuid.test"
    )


@pytest.mark.asyncio
async def test_upload_file_s3_error(mock_s3_client):
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.csv"
    mock_file.file = MagicMock()
    mock_s3_client.upload_fileobj.side_effect = ClientError(
        {"Error": {"Message": "S3 error"}}, "upload_fileobj"
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await upload_file(mock_file)
    assert exc_info.value.status_code == 500
    assert "S3 upload failed: S3 error" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_upload_file_unexpected_error(mock_s3_client):
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test.csv"
    mock_file.file = MagicMock()
    mock_s3_client.upload_fileobj.side_effect = Exception("Unexpected error")

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await upload_file(mock_file)
    assert exc_info.value.status_code == 500
    assert "An unexpected error occurred: Unexpected error" in str(
        exc_info.value.detail
    )


@pytest.mark.asyncio
async def test_upload_file_empty_filename(mock_s3_client):
    # Arrange
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = ""
    mock_file.file = MagicMock()

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await upload_file(mock_file)
    assert exc_info.value.status_code == 400
    assert "File name is required" in str(exc_info.value.detail)
