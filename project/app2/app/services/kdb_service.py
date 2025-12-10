from typing import List, Dict, Any
import asyncio
from qpython import qconnection
from qpython.qcollection import QTable

from app.schemas.kdb import KDBQueryRequest, KDBFilter
from app.core.exceptions import KDBQueryError, InvalidKDBQuery

class KDBService:
    def __init__(self, q_conn: qconnection.QConnection):
        self.q_conn = q_conn

    async def _format_q_value(self, value: Any) -> str:
        if isinstance(value, str):
            # Basic sanitization: escape double quotes, then wrap in double quotes
            return f'\"{value.replace("\"", "\\\"")}\"' # "value" or "value with \"quote\""
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, bool):
            return '1b' if value else '0b'
        elif isinstance(value, list):
            # Recursively format list elements and join with semicolons for Q list
            formatted_elements = []
            for item in value:
                formatted_elements.append(await self._format_q_value(item))
            return f'({';'.join(formatted_elements)})'
        # Add more type handling as needed (e.g., datetime, date)
        # For simplicity, treat others as strings for now, but this is a potential source of error
        return f'\"{str(value).replace("\"", "\\\"")}\"' # Fallback to string quoting

    async def _build_q_query(self, query_request: KDBQueryRequest) -> str:
        select_fields = query_request.fields
        source_table = query_request.source_table
        filters = query_request.filters

        # Basic validation for table and field names
        # In a production system, these should be whitelisted or strictly validated
        # to prevent injection, as direct string interpolation of table/field names is risky.
        if not all(f.isalnum() or f == '.' for f in select_fields + [source_table]):
             raise InvalidKDBQuery(detail="Table or field names contain invalid characters.")

        select_clause = ','.join(select_fields)

        where_clauses = []
        if filters:
            for f in filters:
                formatted_value = await self._format_q_value(f.value)
                operator = f.operator

                if operator == 'in':
                    # Q's 'in' is actually `value within list` or `list contains value`
                    # (value in list) in kdb is `value in list`
                    # For `sym in ("IBM";"GOOG")` we use `sym within list`
                    where_clauses.append(f'{f.field} within {formatted_value}')
                elif operator == '!=':
                    where_clauses.append(f'{f.field} <> {formatted_value}')
                else:
                    where_clauses.append(f'{f.field} {operator} {formatted_value}')

        if where_clauses:
            where_clause = ','.join(where_clauses)
            q_query = f"select {select_clause} from {source_table} where {where_clause}"
        else:
            q_query = f"select {select_clause} from {source_table}"

        return q_query

    async def execute_query(self, query_request: KDBQueryRequest) -> List[Dict[str, Any]]:
        q_query = await self._build_q_query(query_request)
        print(f"Executing KDB+ query: {q_query}")

        try:
            # qPython's sendSync is blocking, use asyncio.to_thread
            result = await asyncio.to_thread(self.q_conn.sendSync, q_query)

            if result is None:
                return []

            if isinstance(result, QTable):
                # Convert QTable to a list of dictionaries
                data_dicts = []
                for i in range(len(result.columns[0])):
                    row_dict = {col.decode('utf-8'): result[col][i] for col in result.columns}
                    data_dicts.append(row_dict)
                return data_dicts
            else:
                # Handle scalar results or other KDB+ types if necessary
                # For now, if not a table, return as a single item list if it makes sense
                # or raise an error if expecting only table results.
                return [{"$result": result}]
        except Exception as e:
            raise KDBQueryError(detail=f"KDB+ query execution failed: {e}")
