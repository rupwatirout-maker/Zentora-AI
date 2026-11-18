"""Business logic for user settings."""

from sqlalchemy.orm import Session

from app.models.settings import Settings
from app.repositories.settings_repository import SettingsRepository
from app.schemas.settings_schema import SettingsUpdate


class SettingsService:
    """Handles user settings operations."""

    @staticmethod
    def create_settings(
        db: Session,
        user_id: int,
    ) -> Settings:
        """Create default settings for a user."""

        settings = Settings(
            user_id=user_id,
        )

        return SettingsRepository.create(
            db=db,
            settings=settings,
        )

    @staticmethod
    def get_settings(
        db: Session,
        user_id: int,
    ) -> Settings | None:
        """Return a user's settings."""

        return SettingsRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def update_settings(
        db: Session,
        settings: Settings,
        data: SettingsUpdate,
    ) -> Settings:
        """Update user settings."""

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(settings, field, value)

        return SettingsRepository.update(
            db=db,
            settings=settings,
        )

    @staticmethod
    def delete_settings(
        db: Session,
        user_id: int,
    ) -> bool:
        """Delete a user's settings."""

        settings = SettingsRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if settings is None:
            return False

        SettingsRepository.delete(
            db=db,
            settings=settings,
        )

        return True