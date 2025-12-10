import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class PreferenceData(BaseModel):
    # This model is flexible for JSONB content
    # It can be as complex as needed, or simply a generic dict
    # For this example, we'll keep it flexible.
    class Config:
        extra = "allow"

    # Example fields, can be extended or replaced by arbitrary JSON
    theme: Optional[str] = None
    notifications: Optional[Dict[str, Any]] = None

class UserPreferenceCreate(BaseModel):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier for the user.")
    preferences: Dict[str, Any] = Field(..., description="JSON object containing user preferences.")

class UserPreferenceResponse(BaseModel):
    user_id: uuid.UUID = Field(..., description="Unique identifier for the user.")
    preferences: Dict[str, Any] = Field(..., description="JSON object containing user preferences.")
    created_at: datetime = Field(..., description="Timestamp when the preferences were created.")
    updated_at: datetime = Field(..., description="Timestamp when the preferences were last updated.")
