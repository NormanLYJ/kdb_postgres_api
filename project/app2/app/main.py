from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from app.api import kdb, preferences
from app.core.config import settings
from app.db.postgres_connector import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    yield
    # Shutdown logic (if any)
    pass

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION, lifespan=lifespan)

# Include API routers
app.include_router(kdb.router, prefix="/api/v1/kdb", tags=["KDB+"])
app.include_router(preferences.router, prefix="/api/v1/preferences", tags=["User Preferences"])

@app.get("/health", response_class=HTMLResponse, summary="Health check endpoint")
async def health_check():
    return "<html><body><h1>Service is healthy!</h1></body></html>"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
