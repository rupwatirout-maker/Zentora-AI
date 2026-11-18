"""Business logic for administrator operations."""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.database import engine
from app.models.chat import Chat
from app.models.history import History
from app.models.profile import Profile
from app.models.uploaded_file import UploadedFile
from app.models.user import User


class AdminService:
    """Business logic for administrator operations."""

    @staticmethod
    def get_dashboard(db: Session) -> dict:
        """Return aggregate application statistics."""

        return {
            "total_users": db.query(User).count(),
            "total_profiles": db.query(Profile).count(),
            "total_chats": db.query(Chat).count(),
            "total_history": db.query(History).count(),
            "total_uploaded_files": db.query(UploadedFile).count(),
        }

    @staticmethod
    def get_all_users(db: Session) -> list[User]:
        """Return user records; response schemas control exposed fields."""

        return (
            db.query(User)
            .order_by(User.id.desc())
            .all()
        )

    @staticmethod
    def get_user(db: Session, user_id: int) -> User | None:
        """Return a user by ID."""

        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int,
        actor_user_id: int,
    ) -> bool:
        """Delete a user without allowing self-deletion or removal of the last admin."""

        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return False

        if user.id == actor_user_id:
            raise ValueError("Administrators cannot delete their own account.")

        if (user.role or "").strip().lower() == "admin":
            admin_count = (
                db.query(User)
                .filter(func.lower(User.role) == "admin")
                .count()
            )

            if admin_count <= 1:
                raise ValueError("The last administrator account cannot be deleted.")

        try:
            db.delete(user)
            db.commit()
        except Exception:
            db.rollback()
            raise

        return True

    @staticmethod
    def get_system_info() -> dict:
        """Return non-sensitive runtime information."""

        return {
            "backend": "FastAPI",
            "database": engine.dialect.name,
            "ai_provider": settings.AI_PROVIDER,
            "status": "Running",
            "version": "1.0.0",
        }
