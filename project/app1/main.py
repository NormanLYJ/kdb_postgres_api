from fastapi import FastAPI
from app.routes.transactions import router as transaction_router
from app.routes.preferences import router as preference_router

app = FastAPI()

app.include_router(transaction_router, prefix="/api")
app.include_router(preference_router, prefix="/api")