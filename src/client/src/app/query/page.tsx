"use client";
import React, { useState, useEffect } from "react";
import apiService from "@/services/api";
import { QueryRequest, QueryResponse, Table as TableModel } from "@/types/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import CodeMirror from "@uiw/react-codemirror";
import { StreamLanguage } from "@codemirror/language";
import { sql, SQLNamespace } from "@codemirror/lang-sql";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const QueryPage = () => {
  const [query, setQuery] = useState("");
  const [queryResult, setQueryResult] = useState<any>({});
  const [queryExecutionId, setQueryExecutionId] = useState<string | null>(null);
  const [queryStatus, setQueryStatus] = useState<string>("Not Started");
  const [tables, setTables] = useState<TableModel[]>([]);

  const handleQueryChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setQuery(e.target.value);
  };

  const handleRunQuery = async () => {
    try {
      setQueryResult(null);
      const queryRequest: QueryRequest = { query };
      const response = await apiService.runQuery(queryRequest);
      setQueryExecutionId(response.query_execution_id || null);
      setQueryStatus("Running");
    } catch (error) {
      console.error("Error running query:", error);
    }
  };

  useEffect(() => {
    const fetchTables = async () => {
      try {
        const response = await apiService.getTables();
        setTables(response.tables);
      } catch (error) {
        console.error("Error fetching tables:", error);
      }
    };

    fetchTables();
  }, []);

  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null;

    const fetchQueryStatus = async () => {
      if (queryExecutionId) {
        try {
          const response = await apiService.getQueryStatus(queryExecutionId);
          setQueryStatus(response.status || "Unknown");

          if (response.status === "SUCCEEDED") {
            const resultsResponse = await apiService.getQueryResults(
              queryExecutionId
            );
            setQueryResult(resultsResponse.results || {});
            clearInterval(intervalId!);
          } else if (response.status === "FAILED") {
            clearInterval(intervalId!);
          }
        } catch (error) {
          console.error("Error fetching query status:", error);
        }
      }
    };

    if (queryExecutionId) {
      intervalId = setInterval(fetchQueryStatus, 5000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [queryExecutionId]);

  const defineSchema = (tables: TableModel[]): SQLNamespace => {
    const schema: any = {};
    const headers = queryResult?.headers?.reduce(
      (acc: Record<string, any>, header: string) => {
        acc[header] = {};
        return acc;
      },
      {}
    );
    console.log(headers);
    tables.forEach((table: TableModel) => {
      schema[table.DatabaseName] = schema[table.DatabaseName] || {
        [table.Name]: headers ? headers : {},
      };
    });
    return schema;
  };

  return (
    <div className="flex h-full">
      <div className="flex-1 p-4">
        <h1 className="text-lg font-semibold mb-4">Run Query</h1>
        <CodeMirror
          indentWithTab={true}
          className="text-wrap code-mirror flex min-h-[60px] border-input text-sm shadow-sm border rounded"
          value={query}
          onChange={(value) => setQuery(value)}
          height="200px"
          width="100%"
          extensions={[
            sql({
              schema: defineSchema(tables),
              // tables: tables.map((table) => ({ label: table.Name })),
            }),
          ]}
        />
        <div className="flex items-center	flex-row justify-between">
          <Button
            onClick={handleRunQuery}
            disabled={!query}
            className="mt-4 px-4 py-2"
          >
            Run Query
          </Button>
          <p className="py-2 text-sm font-medium leading-none text-gray-500">
            Status: {queryStatus}
          </p>
        </div>
        {queryResult?.data && (
          <div className="mt-6 max-h-80 overflow-auto border rounded-sm">
            <Table>
              <TableCaption>Query Results</TableCaption>
              <TableHeader>
                <TableRow>
                  {queryResult.headers.map((header: string) => (
                    <TableHead className="capitalize" key={header}>
                      {header.split("_").join(" ")}
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {queryResult?.data.map((row: any[], index: number) => (
                  <TableRow key={index}>
                    {row.map((cell: any, cellIndex: number) => (
                      <TableCell key={`${index}-${cellIndex}`}>
                        {cell}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
      <div className="w-1/3 p-4 border-l overflow-auto">
        <h2 className="text-lg font-semibold mb-4">Available Tables</h2>
        <ul>
          {tables?.map((table, index) => (
            <li key={index} className="mb-2 w-full">
              <Button
                size="sm"
                className="break-words"
                variant="link"
                onClick={() =>
                  setQuery(
                    `SELECT * from "${table.DatabaseName}"."${table.Name}" limit 100`
                  )
                }
              >
                {table.DatabaseName}.{table.Name}
              </Button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default QueryPage;
