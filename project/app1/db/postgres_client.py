import asyncpg
import json

class AsyncPostgresClient:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        """Initialize asyncpg connection pool"""
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=1,
                max_size=10,
                command_timeout=5
            )

    async def get_user_preferences(self, user_id: str):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT preferences FROM user_preferences WHERE user_id = $1",
                user_id
            )
            return row["preferences"] if row else {}

    async def save_user_preferences(self, user_id: str, preferences: dict):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_preferences (user_id, preferences)
                VALUES ($1, $2)
                ON CONFLICT (user_id) DO UPDATE
                SET preferences = EXCLUDED.preferences
            """, user_id, preferences)   # asyncpg automatically handles JSON