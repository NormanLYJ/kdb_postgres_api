import os

POSTGRES_DSN = os.getenv(
    "DATABASE_URL",
    "postgres://postgres:admin@localhost:5432/mydb"
)

KDB_HOST = os.getenv("KDB_HOST", "localhost")
KDB_PORT = int(os.getenv("KDB_PORT", "5000"))
