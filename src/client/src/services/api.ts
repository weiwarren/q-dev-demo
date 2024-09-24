import axios, {
  AxiosInstance,
  AxiosRequestConfig,
  InternalAxiosRequestConfig,
} from "axios";
import {
  FileUploadRequest,
  FileUploadResponse,
  FilePreviewRequest,
  FilePreviewResponse,
  SubmitDataRequest,
  SubmitDataResponse,
  QueryRequest,
  QueryResponse,
  Table,
} from "@/types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

class ApiService {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Add a request interceptor
    this.axiosInstance.interceptors.request.use(
      (config: AxiosRequestConfig) => {
        // Add any additional headers or configurations here
        const token = localStorage.getItem("accessToken");
        if (token) {
          config.headers!.Authorization = `Bearer ${token}`;
        }
        return config as InternalAxiosRequestConfig;
      },
      (error) => Promise.reject(error)
    );

    // Add a response interceptor
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error) => {
        // Handle error responses here
        if (error.response && error.response.status === 401) {
          // Handle unauthorized error
          // e.g., redirect to login page
        }
        return Promise.reject(error);
      }
    );
  }

  public uploadFile(
    fileUploadRequest: FileUploadRequest
  ): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append("file", fileUploadRequest.file);

    return this.axiosInstance
      .post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => response.data);
  }

  public previewFile(
    filePreviewRequest: FilePreviewRequest
  ): Promise<FilePreviewResponse> {
    return this.axiosInstance
      .post("/preview", filePreviewRequest)
      .then((response) => response.data);
  }

  public submitJob(
    submitDataRequest: SubmitDataRequest
  ): Promise<SubmitDataResponse> {
    return this.axiosInstance
      .post("/submit", submitDataRequest)
      .then((response) => response.data);
  }

  public getJobStatus(jobId: string): Promise<any> {
    return this.axiosInstance
      .get(`/job/${jobId}/status`)
      .then((response) => response.data);
  }
  public runQuery(queryRequest: QueryRequest): Promise<QueryResponse> {
    return this.axiosInstance
      .post("/query", queryRequest)
      .then((response) => response.data);
  }

  public getTables(): Promise<{ tables: Table[] }> {
    return this.axiosInstance.get("/tables").then((response) => response.data);
  }

  public getQueryStatus(queryExecutionId: string): Promise<QueryResponse> {
    return this.axiosInstance
      .get(`/query/${queryExecutionId}/status`)
      .then((response) => response.data);
  }

  public getQueryResults(queryExecutionId: string): Promise<any> {
    return this.axiosInstance
      .get(`/query/${queryExecutionId}/results`)
      .then((response) => response.data);
  }
}

const apiService = new ApiService();

export default apiService;
