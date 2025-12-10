from typing import AsyncGenerator
from fastapi import Depends
import asyncio

from qpython import qconnection
from qpython.qcollection import QTable
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import KDBConnectionError, PostgresConnectionError
from app.db.postgres_connector import AsyncSessionLocal

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            print(f"Database session error: {e}")
            raise PostgresConnectionError(detail=f"Failed to get database session: {e}")

async def get_kdb_connection() -> AsyncGenerator[qconnection.QConnection, None]:
    # QConnection is synchronous, so we ensure it's run in a separate thread
    # to avoid blocking the asyncio event loop.
    q_conn = None
    try:
        q_conn = await asyncio.to_thread(qconnection.QConnection, host=settings.KDB_HOST, port=settings.KDB_PORT)
        await asyncio.to_thread(q_conn.open)
        yield q_conn
    except Exception as e:
        print(f"KDB+ connection error: {e}")
        raise KDBConnectionError(detail=f"Failed to connect to KDB+: {e}")
    finally:
        if q_conn and q_conn.is_connected():
            await asyncio.to_thread(q_conn.close)

KDBConnectionDep = Depends(get_kdb_connection)
DatabaseSessionDep = Depends(get_db_session)
