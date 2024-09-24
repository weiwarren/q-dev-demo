"use client";
import React, { useEffect, useState, Suspense } from "react";
import apiService from "@/services/api";
import { useRouter, useSearchParams } from "next/navigation";
import { FilePreviewResponse } from "@/types/api";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Separator } from "@radix-ui/react-separator";

const PreviewPage = () => {
  const [previewData, setPreviewData] = useState<FilePreviewResponse>();
  const router = useRouter();
  const searchParams = useSearchParams();
  const fileKey = searchParams?.get("fileKey");

  useEffect(() => {
    if (fileKey) {
      const fetchPreviewData = async () => {
        try {
          const data = await apiService.previewFile({
            file_key: fileKey as string,
          });
          setPreviewData(data);
        } catch (error) {
          console.error("Error fetching preview data:", error);
        }
      };
      fetchPreviewData();
    }
  }, [fileKey]);

  const handleSubmit = async () => {
    try {
      const response = await apiService.submitJob({ file_key: fileKey! });
      router.push(`/job-status?jobId=${response.job_id}`);
    } catch (error) {
      console.error("Error submitting job:", error);
    }
  };

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div className="flex flex-col">
        <h1 className="mb-6">Preview {fileKey?.split("/")[1]}</h1>
        <div className="flex-1 max-h-96 overflow-auto">
          {previewData && previewData.data && (
            <Table>
              <TableHeader>
                <TableRow>
                  {previewData.headers.map((header) => (
                    <TableHead key={header}>{header}</TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {previewData.data.map((row, index) => (
                  <TableRow key={index}>
                    {previewData.headers.map((header, index) => (
                      <TableCell key={`${index}-${header}`}>
                        {row[index]}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </div>
        <Separator className="my-6"></Separator>
        <div>
          <Button onClick={handleSubmit}>Submit</Button>
        </div>
      </div>
    </Suspense>
  );
};

export default PreviewPage;
