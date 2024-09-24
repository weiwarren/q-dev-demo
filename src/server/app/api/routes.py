from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from app.api.schemas import (
    FileUploadResponse,
    FilePreviewRequest,
    FilePreviewResponse,
    QueryRequest,
    QueryResponse,
    SubmitJobRequest,
)
from app.services.glue_service import (
    get_crawled_tables_from_database,
    submit_crawler_job,
    get_crawler_job_status,
)
from app.services.file_service import FileService
from app.services.query_service import QueryService

router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    file_service = FileService()
    file_key = await file_service.upload_file(file)
    return {"file_key": file_key}


@router.post("/preview", response_model=FilePreviewResponse)
async def preview_file(
    request: FilePreviewRequest, file_service: FileService = Depends()
):
    preview_data = await file_service.preview_file(request.file_key)
    print(preview_data)
    return FilePreviewResponse(**preview_data)


@router.post("/submit")
async def submit_job(request: SubmitJobRequest):
    job_id = submit_crawler_job(request.file_key)
    return {"job_id": job_id}


@router.get("/job/{job_id}/status")
async def get_job_status(job_id: str):
    job_status = get_crawler_job_status(job_id)
    return {"job_status": job_status}


@router.get("/tables")
async def get_crawled_tables():
    """
    Get a list of crawled tables from a database in AWS Glue.

    Args:
        database_name (str): The name of the database.

    Returns:
        List[Dict]: A list of dictionaries containing table details.
    """
    try:
        tables = get_crawled_tables_from_database()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException()(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def run_query(request: QueryRequest, query_service: QueryService = Depends()):
    """
    Run a query against the catalog.
    """
    query_execution_id = query_service.run_query(request.query)
    return {"query_execution_id": query_execution_id}


@router.get("/query/{query_execution_id}/status", response_model=QueryResponse)
async def get_query_status(
    query_execution_id: str, query_service: QueryService = Depends()
):
    """
    Get the status of a query execution.
    """
    status = query_service.get_query_status(query_execution_id)
    return {"status": status}


@router.get("/query/{query_execution_id}/results")
async def get_query_results(
    query_execution_id: str, query_service: QueryService = Depends()
):
    """
    Get the results of a query execution.
    """
    results = query_service.get_query_results(query_execution_id)
    return {"results": results}
