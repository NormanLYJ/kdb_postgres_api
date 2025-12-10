from typing import List, Any, Literal, Optional
from pydantic import BaseModel, Field

class KDBFilter(BaseModel):
    field: str = Field(..., description="The field name to filter on.")
    operator: Literal['=', '!=', '>', '<', '>=', '<=', 'in'] = Field(..., description="The comparison operator.")
    value: Any = Field(..., description="The value to compare against. Can be a scalar or a list for 'in' operator.")

class KDBQueryRequest(BaseModel):
    source_table: str = Field(..., description="The name of the KDB+ table to query.")
    fields: List[str] = Field(..., description="A list of field names to select.")
    filters: Optional[List[KDBFilter]] = Field(None, description="Optional list of filter conditions.")

class KDBQueryResponse(BaseModel):
    status: str = Field("success", description="Status of the query operation.")
    data: List[dict] = Field(..., description="The query results as a list of dictionaries.")
    message: Optional[str] = Field(None, description="Optional message regarding the query.")
