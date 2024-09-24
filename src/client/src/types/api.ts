export interface FileUploadRequest {
  file: File;
}

export interface FileUploadResponse {
  file_key: string;
}

export interface FilePreviewRequest {
  file_key: string;
}

export interface FilePreviewResponse {
  headers: string[];
  data: any[][];
}

// @/types/api.ts
export interface SubmitDataRequest {
  file_key: string;
}
// @/types/api.ts
export interface SubmitDataResponse {
  job_id: string;
}

export interface Table {
  Name: string;
  DatabaseName: string;
  // Add any other properties you need for table details
}
export interface QueryRequest {
  query: string;
}

export interface QueryResponse {
  query_execution_id?: string;
  status?: string;
  results?: Record<string, string[]>;
}
