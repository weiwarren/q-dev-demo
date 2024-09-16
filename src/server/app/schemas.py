from pydantic import BaseModel
from typing import List, Dict, Any

class UploadResponse(BaseModel):
    file_id: str
    message: str

class PreviewResponse(BaseModel):
    data: List[Dict[str, Any]]
    columns: List[str]

class SubmitResponse(BaseModel):
    job_id: str
    message: str

class JobStatusResponse(BaseModel):
    status: str
    message: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    results: List[Dict[str, Any]]
    columns: List[str]

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
