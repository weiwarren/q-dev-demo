"use client";
import React, { useState } from "react";
import apiService from "@/services/api";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const UploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const router = useRouter();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (file) {
      try {
        const response = await apiService.uploadFile({ file });
        router.push(`/preview?fileKey=${response.file_key}`);
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload CSV</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <Input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            placeholder="Select a CSV file"
          />
        </div>
        <Button onClick={handleUpload} disabled={!file}>
          Upload
        </Button>
      </CardContent>
    </Card>
  );
};

export default UploadPage;
