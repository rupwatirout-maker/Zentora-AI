"""Authenticated user settings endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.settings_schema import SettingsResponse, SettingsUpdate
from app.services.settings_service import SettingsService


router = APIRouter(
    prefix="/api/settings",
    tags=["Settings"],
)


def verify_settings_owner(user_id: int, current_user: User) -> None:
    """Prevent users from accessing another account's settings."""

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access another user's settings.",
        )


@router.get("/{user_id}", response_model=SettingsResponse)
def get_user_settings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_settings_owner(user_id, current_user)

    settings = SettingsService.get_settings(db, current_user.id)

    if settings is None:
        settings = SettingsService.create_settings(db, current_user.id)

    return settings


@router.put("/{user_id}", response_model=SettingsResponse)
def update_user_settings(
    user_id: int,
    data: SettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_settings_owner(user_id, current_user)

    settings = SettingsService.get_settings(db, current_user.id)

    if settings is None:
        settings = SettingsService.create_settings(db, current_user.id)

    return SettingsService.update_settings(db, settings, data)


@router.delete("/{user_id}")
def delete_user_settings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_settings_owner(user_id, current_user)

    deleted = SettingsService.delete_settings(db, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settings not found.",
        )

    return {"message": "Settings deleted successfully."}


@router.get("/")
def get_application_settings():
    """Return non-sensitive public application metadata."""

    return {
        "project": "Velora AI",
        "version": "1.0.0",
        "ai_provider": "Ollama",
        "database": "SQLite",
    }