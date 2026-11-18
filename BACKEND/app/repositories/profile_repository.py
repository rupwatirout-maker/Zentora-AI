"""Database operations for user profiles."""

from sqlalchemy.orm import Session

from app.models.profile import Profile


class ProfileRepository:
    """Provides database access for profile records."""

    @staticmethod
    def create(
        db: Session,
        profile: Profile,
    ) -> Profile:
        """Create a profile."""

        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def get_by_id(
        db: Session,
        profile_id: int,
    ) -> Profile | None:
        """Return a profile by ID."""

        return (
            db.query(Profile)
            .filter(Profile.id == profile_id)
            .first()
        )

    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: int,
    ) -> Profile | None:
        """Return a profile for a user."""

        return (
            db.query(Profile)
            .filter(Profile.user_id == user_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        profile: Profile,
    ) -> Profile:
        """Save profile changes."""

        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def delete(
        db: Session,
        profile: Profile,
    ) -> None:
        """Delete a profile."""

        db.delete(profile)
        db.commit()