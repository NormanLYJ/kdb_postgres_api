import uuid
from datetime import datetime
from typing import Any
from sqlalchemy import Column, DateTime, UUID, JSON
from app.db.postgres_connector import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    user_id: Column[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    preferences: Column[Any] = Column(JSON, nullable=False) # JSONB column
    created_at: Column[datetime] = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Column[datetime] = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserPreference(user_id='{self.user_id}', preferences='{self.preferences}')>"
