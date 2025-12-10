import uuid
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from app.db.models import UserPreference
from app.schemas.preferences import UserPreferenceCreate, UserPreferenceResponse
from app.core.exceptions import PreferenceNotFound

class UserPreferenceService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_preference(self, user_id: uuid.UUID) -> UserPreferenceResponse:
        stmt = select(UserPreference).where(UserPreference.user_id == user_id)
        result = await self.db_session.execute(stmt)
        preference = result.scalar_one_or_none()
        if not preference:
            raise PreferenceNotFound(f"Preferences for user_id {user_id} not found.")
        return UserPreferenceResponse.model_validate(preference)

    async def create_or_update_preference(self, pref_data: UserPreferenceCreate) -> UserPreferenceResponse:
        # Check if preference for user_id already exists
        stmt = select(UserPreference).where(UserPreference.user_id == pref_data.user_id)
        existing_pref = (await self.db_session.execute(stmt)).scalar_one_or_none()

        if existing_pref:
            # Update existing preferences
            update_stmt = update(UserPreference).where(UserPreference.user_id == pref_data.user_id).values(
                preferences=pref_data.preferences
            ).returning(UserPreference)
            result = await self.db_session.execute(update_stmt)
            updated_preference = result.scalar_one()
            await self.db_session.commit()
            return UserPreferenceResponse.model_validate(updated_preference)
        else:
            # Insert new preferences
            new_preference = UserPreference(user_id=pref_data.user_id, preferences=pref_data.preferences)
            self.db_session.add(new_preference)
            await self.db_session.commit()
            await self.db_session.refresh(new_preference)
            return UserPreferenceResponse.model_validate(new_preference)
