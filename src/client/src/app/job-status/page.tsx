"use client";
import React, { useEffect, useState } from "react";
import apiService from "@/services/api";
import { useRouter, useSearchParams } from "next/navigation";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";

const JobStatusPage = () => {
  const [jobStatus, setJobStatus] = useState<string>("");
  const router = useRouter();
  const searchParams = useSearchParams();
  const jobId = searchParams.get("jobId");

  useEffect(() => {
    if (jobId) {
      const fetchJobStatus = async () => {
        try {
          const response = await apiService.getJobStatus(jobId as string);
          setJobStatus(response.job_status);
        } catch (error) {
          console.error("Error fetching job status:", error);
        }
      };
      const interval = setInterval(fetchJobStatus, 5000);
      return () => clearInterval(interval);
    }
  }, [jobId]);

  const handleRunQuery = () => {
    router.push("/query");
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Job Status</CardTitle>
        <CardDescription>Check the status of your job here.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <p>Job ID: {jobId}</p>
        {jobStatus === "" ? (
          <Skeleton className="h-6 w-64" />
        ) : jobStatus === "READY" ? (
          <Alert className="bg-green-100 text-green-800 space-y-4">
            <AlertTitle>Job Succeeded</AlertTitle>
            <AlertDescription>
              Your job has completed successfully.
            </AlertDescription>
            <Button onClick={handleRunQuery}>Run Query</Button>
          </Alert>
        ) : jobStatus === "FAILED" ? (
          <Alert className="bg-red-100 text-red-800">
            <AlertTitle>Job Failed</AlertTitle>
            <AlertDescription>
              Your job has failed. Please try again.
            </AlertDescription>
          </Alert>
        ) : jobStatus === "RUNNING" ? (
          <Alert className="bg-blue-100 text-blue-800">
            <AlertTitle>Job Running</AlertTitle>
            <AlertDescription>
              Your job is currently running. Please wait...
            </AlertDescription>
          </Alert>
        ) : (
          <Alert className="bg-yellow-100 text-yellow-800">
            <AlertTitle>Job Status: {jobStatus}</AlertTitle>
            <AlertDescription>Your job status is {jobStatus}.</AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default JobStatusPage;
