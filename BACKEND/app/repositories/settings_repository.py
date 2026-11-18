"""Database operations for user settings."""

from sqlalchemy.orm import Session

from app.models.settings import Settings


class SettingsRepository:
    """Provides database access for user settings."""

    @staticmethod
    def create(
        db: Session,
        settings: Settings,
    ) -> Settings:
        """Create user settings."""

        db.add(settings)
        db.commit()
        db.refresh(settings)
        return settings

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int,
    ) -> Settings | None:
        """Return settings for a user."""

        return (
            db.query(Settings)
            .filter(Settings.user_id == user_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        settings: Settings,
    ) -> Settings:
        """Save settings changes."""

        db.commit()
        db.refresh(settings)
        return settings

    @staticmethod
    def delete(
        db: Session,
        settings: Settings,
    ) -> None:
        """Delete user settings."""

        db.delete(settings)
        db.commit()