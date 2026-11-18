"""Request and response schemas for user profiles."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    """Schema for creating a profile."""

    full_name: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None


class ProfileUpdate(BaseModel):
    """Schema for updating a profile."""

    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None


class ProfileResponse(BaseModel):
    """Schema for profile details."""

    id: int
    user_id: int
    full_name: Optional[str]
    phone: Optional[str]
    bio: Optional[str]
    avatar: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)