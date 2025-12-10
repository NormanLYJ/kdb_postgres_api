from fastapi import APIRouter, status, Depends
from typing import List, Dict, Any
from qpython.qconnection import QConnection

from app.schemas.kdb import KDBQueryRequest, KDBQueryResponse
from app.services.kdb_service import KDBService
from app.core.dependencies import KDBConnectionDep
from app.core.exceptions import KDBConnectionError, KDBQueryError, InvalidKDBQuery

router = APIRouter()

@router.post("/query", response_model=KDBQueryResponse, status_code=status.HTTP_200_OK,
             summary="Execute a dynamic KDB+ q-SQL query",
             responses={
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "KDB+ connection or query error"},
                 status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Invalid KDB+ query parameters"}
             })
async def query_kdb(query_request: KDBQueryRequest, q_conn: QConnection = KDBConnectionDep) -> KDBQueryResponse:
    """Accepts a JSON body to dynamically construct and execute a KDB+ q-SQL query."""
    kdb_service = KDBService(q_conn)
    try:
        results = await kdb_service.execute_query(query_request)
        return KDBQueryResponse(data=results)
    except (KDBConnectionError, KDBQueryError, InvalidKDBQuery) as e:
        raise e # Re-raise custom HTTPExceptions
    except Exception as e:
        raise KDBQueryError(detail=f"An unexpected error occurred during KDB+ query: {e}")
