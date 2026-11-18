"""Business logic for user profiles."""

from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.repositories.profile_repository import ProfileRepository


class ProfileService:
    """Handles profile operations."""

    @staticmethod
    def create_profile(
        db: Session,
        user_id: int,
        full_name: str,
        phone: str | None = None,
        bio: str | None = None,
        avatar: str | None = None,
    ) -> Profile:
        """Create a profile."""

        profile = Profile(
            user_id=user_id,
            full_name=full_name,
            phone=phone,
            bio=bio,
            avatar=avatar,
        )

        return ProfileRepository.create(
            db=db,
            profile=profile,
        )

    @staticmethod
    def get_profile(
        db: Session,
        user_id: int,
    ) -> Profile | None:
        """Return a user's profile."""

        return ProfileRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def update_profile(
        db: Session,
        profile: Profile,
        data,
    ) -> Profile:
        """Update a profile."""

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(profile, field, value)

        return ProfileRepository.update(
            db=db,
            profile=profile,
        )

    @staticmethod
    def delete_profile(
        db: Session,
        user_id: int,
    ) -> bool:
        """Delete a user's profile."""

        profile = ProfileRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        if profile is None:
            return False

        ProfileRepository.delete(
            db=db,
            profile=profile,
        )

        return True