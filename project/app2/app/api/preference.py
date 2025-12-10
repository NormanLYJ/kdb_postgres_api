import uuid
from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.preferences import UserPreferenceCreate, UserPreferenceResponse
from app.services.preference_service import UserPreferenceService
from app.core.dependencies import DatabaseSessionDep
from app.core.exceptions import PreferenceNotFound, PostgresConnectionError

router = APIRouter()

@router.post(
    "/",
    response_model=UserPreferenceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create or update user preferences",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "PostgreSQL database error"}
    }
)
async def create_or_update_user_preference(
    pref_data: UserPreferenceCreate,
    db_session: AsyncSession = DatabaseSessionDep
) -> UserPreferenceResponse:
    """Creates new user preferences or updates existing ones based on user_id."""
    try:
        service = UserPreferenceService(db_session)
        preference = await service.create_or_update_preference(pref_data)
        return preference
    except Exception as e:
        raise PostgresConnectionError(detail=f"Failed to create/update preference: {e}")

@router.get(
    "/{user_id}",
    response_model=UserPreferenceResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve user preferences",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User preferences not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "PostgreSQL database error"}
    }
)
async def get_user_preference(
    user_id: uuid.UUID = Path(..., description="The UUID of the user."),
    db_session: AsyncSession = DatabaseSessionDep
) -> UserPreferenceResponse:
    """Retrieves user preferences by user ID."""
    try:
        service = UserPreferenceService(db_session)
        preference = await service.get_preference(user_id)
        return preference
    except PreferenceNotFound as e:
        raise e # Re-raise custom HTTPException
    except Exception as e:
        raise PostgresConnectionError(detail=f"Failed to retrieve preference: {e}")
