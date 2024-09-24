import pytest
from fastapi.testclient import TestClient
from app.main import app
import logging
from unittest.mock import patch, AsyncMock
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TestClient(app, base_url="http://testserver/api/v1")


def test_upload_file():
    # Create a test file
    test_file = b"""date,country_code,new_confirmed,new_deceased,cumulative_confirmed,cumulative_deceased,new_persons_fully_vaccinated
7/3/2020,AU,10,0,73,2,0"""

    # Send a POST request to the /upload endpoint
    response = client.post("upload", files={"file": ("test_file.txt", test_file)})
    print("here: ", response.json())
    logger.info("Response JSON: %s", response.json())
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains a file_key
    assert "file_key" in response.json()

def test_preview_file(monkeypatch):
    # Mock the FileService.preview_file method
    async def mock_preview_file(file_key):
        return {"headers": ["col1", "col2"], "data": [["value1", "value2"], ["value3", "value4"]]}

    mock_preview_file = AsyncMock(side_effect=mock_preview_file)
    
    monkeypatch.setattr(
        "app.services.file_service.FileService.preview_file",
        mock_preview_file
    )

    # Send a POST request to the /preview endpoint
    response = client.post("/api/v1/preview", json={"file_key": "test_key"})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the correct headers and data
    response_data = response.json()
    assert "headers" in response_data
    assert "data" in response_data
    assert response_data["headers"] == ["col1", "col2"]
    assert response_data["data"] == [["value1", "value2"], ["value3", "value4"]]
#     # Mock the submit_crawler_job function
#     monkeypatch.setattr("app.api.routes.submit_crawler_job", lambda: "test_job_id")

#     # Send a POST request to the /submit endpoint
#     response = client.post("/submit")

#     # Assert that the response status code is 200 (OK)
#     assert response.status_code == 200

#     # Assert that the response contains the expected job_id
#     assert response.json() == {"job_id": "test_job_id"}

# def test_get_job_status(monkeypatch):
#     # Mock the get_crawler_job_status function
#     monkeypatch.setattr("app.api.routes.get_crawler_job_status", lambda x: "SUCCEEDED")

#     # Send a GET request to the /job/{job_id}/status endpoint
#     response = client.get("/job/test_job_id/status")

#     # Assert that the response status code is 200 (OK)
#     assert response.status_code == 200

#     # Assert that the response contains the expected job_status
#     assert response.json() == {"job_status": "SUCCEEDED"}

# def test_get_crawled_tables(monkeypatch):
#     # Mock the get_crawled_tables_from_database function
#     monkeypatch.setattr("app.services.glue_service.get_crawled_tables_from_database", lambda: ["table1", "table2"])

#     # Send a GET request to the /tables endpoint
#     response = client.get("/tables")

#     # Assert that the response status code is 200 (OK)
#     assert response.status_code == 200
