from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from sqlalchemy import MetaData

# Define the base for declarative models
Base = declarative_base()

# Asynchronous engine
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Asynchronous session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession
)

async def init_db():
    """Initializes the database by creating all tables."""
    async with engine.begin() as conn:
        # Import all models here to ensure they are registered with Base.metadata
        # This prevents issues where models are not known to Base.metadata
        # when create_all is called.
        from app.db import models # noqa: F401
        await conn.run_sync(Base.metadata.create_all)
