import pandas as pd
from typing import Dict, List, Any, Optional
import boto3
from mypy_boto3_athena import AthenaClient
import logging
from app.config import settings


logger = logging.getLogger(__name__)
if settings.ATHENA_ENDPOINT_URL:
    logger.info("Using local athena client")
    athena: AthenaClient = boto3.client("athena", endpoint_url=settings.ATHENA_ENDPOINT_URL)
else:
    athena: AthenaClient = boto3.client("athena")


class QueryService:
    def __init__(self):
        self.data = None

    def run_query(self, query: str) -> Optional[str]:
        """
        Use Athena to run a query against the catalog.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            Optional[str]: The Athena query execution ID if successful, None otherwise.
        """
        try:
            # use athena clien api to execute a query
            response = athena.start_query_execution(
                QueryString=query,
                QueryExecutionContext={"Database": settings.GLUE_CATALOG_DATABASE},
                ResultConfiguration={"OutputLocation": f"s3://{settings.ATHENA_OUTPUT_LOCATION}"},
            )
            return response.get("QueryExecutionId")
        except Exception as e:
            print(f"Error running query: {e}")
            return None

    def get_query_status(self, query_execution_id: str) -> str:
        """
        Get the status of an Athena query execution.

        Args:
            query_execution_id (str): The Athena query execution ID.

        Returns:
            str: The status of the query execution.
        """
        response = athena.get_query_execution(QueryExecutionId=query_execution_id)
        return response["QueryExecution"]["Status"]["State"]


    def get_query_results(self, query_execution_id: str) -> Dict[str, List[str]]:
        """
        Get the results of an Athena query execution.

        Args:
            query_execution_id (str): The Athena query execution ID.

        Returns:
            Dict[str, List[str]]: A dictionary containing the headers and data of the query results.
                The keys are 'headers' and 'data', and the values are lists of strings.
        """
        response = athena.get_query_results(QueryExecutionId=query_execution_id)
        result_set = response.get('ResultSet', {})
        rows = result_set.get('Rows', [])
        
        if not rows:
            return {'headers': [], 'data': []}
        
        if settings.IS_LOCAL:
            start_index = 1
        else:
            start_index = 0
        headers = [col.get('VarCharValue', 'NULL') for col in rows[start_index]['Data']]
        data = []

        for row in rows[start_index+1:]:
            row_data = [col.get('VarCharValue', 'NULL') for col in row['Data']]
            data.append(row_data)

        return {'headers': headers, 'data': data}
