from pydantic import BaseModel
from typing import Dict, List, Any, Optional


# Request and response schemas
# Request and response schemas
class FileUpload(BaseModel):
    file: bytes


class FileUploadResponse(BaseModel):
    file_key: str


class FilePreviewRequest(BaseModel):
    file_key: str


class FilePreviewResponse(BaseModel):
    headers: List[str]
    data: List[List[Any]]

class SubmitJobRequest(BaseModel):
    file_key: str
    
class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query_execution_id: Optional[str] = None
    status: Optional[str] = None
    results: Optional[Dict[str, List[str]]] = None
