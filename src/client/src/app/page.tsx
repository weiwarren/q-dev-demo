"use client";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const HomePage = () => {
  const router = useRouter();
  const handleGetStarted = () => {
    // Replace "/upload" with the path you want to navigate to
    router.push("/upload");
  };
  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Get Started</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="mb-4">
            Welcome to the Simple Data Analytics application! To get started,
            follow these steps:
          </p>
          <ol className="list-decimal pl-4">
            <li>
              Upload your data file using the Upload File option in the
              navigation menu.
            </li>
            <li>Preview your data and ensure its correct.</li>
            <li>Submit a job to analyze your data.</li>
            <li>View the results and insights from the analysis.</li>
          </ol>
          <Button className="mt-4" onClick={handleGetStarted}>
            Get Started
          </Button>
        </CardContent>
      </Card>
    </>
  );
};

export default HomePage;
