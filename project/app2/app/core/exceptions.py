from fastapi import HTTPException, status

class KDBConnectionError(HTTPException):
    def __init__(self, detail: str = "Could not connect to KDB+ instance."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class KDBQueryError(HTTPException):
    def __init__(self, detail: str = "Error executing KDB+ query."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class PostgresConnectionError(HTTPException):
    def __init__(self, detail: str = "Could not connect to PostgreSQL database."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class PreferenceNotFound(HTTPException):
    def __init__(self, detail: str = "User preferences not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class InvalidKDBQuery(HTTPException):
    def __init__(self, detail: str = "Invalid KDB+ query format or parameters."):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
