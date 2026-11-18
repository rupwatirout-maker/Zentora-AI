"""Request and response schemas for chat."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    """Request schema for sending a message."""

    user_id: int
    message: str


class ChatResponse(BaseModel):
    """Response schema for an AI reply."""

    id: int
    user_id: int
    user_message: str
    ai_response: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatHistoryResponse(BaseModel):
    """Schema for chat history records."""

    id: int
    user_message: str
    ai_response: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)