"""Request and response schemas for file uploads."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UploadResponse(BaseModel):
    """Schema returned after a successful upload."""

    id: int
    user_id: int
    original_filename: str
    stored_filename: str
    file_path: str
    file_type: str
    file_size: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FileResponse(BaseModel):
    """Schema for uploaded file details."""

    id: int
    user_id: int
    original_filename: str
    stored_filename: str
    file_path: str
    file_type: str
    file_size: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeleteFileResponse(BaseModel):
    """Schema returned after deleting a file."""

    message: str