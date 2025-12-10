from fastapi import APIRouter, Depends
from app.db.postgres_client import AsyncPostgresClient

router = APIRouter()

pg = AsyncPostgresClient(
    dsn="postgres://postgres:admin@localhost:5432/mydb"
)

@router.on_event("startup")
async def startup():
    await pg.connect()

@router.get("/preferences/{user_id}")
async def get_preferences(user_id: str):
    return await pg.get_user_preferences(user_id)

@router.post("/preferences/{user_id}")
async def save_preferences(user_id: str, prefs: dict):
    await pg.save_user_preferences(user_id, prefs)
    return {"status": "saved"}