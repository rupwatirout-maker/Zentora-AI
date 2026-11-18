"""Schemas for application settings."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SettingsCreate(BaseModel):
    """Request schema for creating settings."""

    theme: str = "light"
    language: str = "en"
    notifications_enabled: bool = True


class SettingsUpdate(BaseModel):
    """Request schema for updating settings."""

    theme: str | None = None
    language: str | None = None
    notifications_enabled: bool | None = None


class SettingsResponse(BaseModel):
    """Response schema for user settings."""

    id: int
    user_id: int
    theme: str
    language: str
    notifications_enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)