from fastapi import APIRouter, Query
from app.db.kdb_client import KDBClient

router = APIRouter()

kdb = KDBClient(host="localhost", port=5000)

@router.get("/transactions")
def get_transactions(start_date: str, end_date: str):
    data = kdb.query_transactions(start_date, end_date)
    return {"transactions": data}
