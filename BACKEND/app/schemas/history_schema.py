"""Schemas for chat history."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HistoryCreate(BaseModel):
    """Request schema for creating a history record."""

    user_id: int
    user_message: str
    ai_response: str


class HistoryResponse(BaseModel):
    """Response schema for a history record."""

    id: int
    user_id: int
    user_message: str
    ai_response: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)