"""Authentication request and response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class UserSignup(BaseModel):
    """Schema for user registration."""

    username: str = Field(
        min_length=3,
        max_length=100,
        validation_alias=AliasChoices("username", "full_name"),
    )
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Username cannot be empty.")
        return value


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for authentication token."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user details."""

    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChangePassword(BaseModel):
    """Schema for password update."""

    old_password: str
    new_password: str


class ForgotPassword(BaseModel):
    """Schema for password reset request."""

    email: EmailStr


class ResetPassword(BaseModel):
    """Schema for password reset."""

    token: str
    new_password: str


class UpdateUser(BaseModel):
    """Schema for updating user information."""

    username: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = ConfigDict(from_attributes=True)