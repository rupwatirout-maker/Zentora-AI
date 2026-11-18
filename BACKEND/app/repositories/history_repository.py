"""Database operations for chat history."""

from sqlalchemy.orm import Session

from app.models.history import History


class HistoryRepository:
    """Provides database access for chat history."""

    @staticmethod
    def create(
        db: Session,
        history: History,
    ) -> History:
        """Create a history record."""

        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def get_by_id(
        db: Session,
        history_id: int,
    ) -> History | None:
        """Return a history record by ID."""

        return (
            db.query(History)
            .filter(History.id == history_id)
            .first()
        )

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int,
    ):
        """Return all history records for a user."""

        return (
            db.query(History)
            .filter(History.user_id == user_id)
            .order_by(History.created_at.desc())
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        history: History,
    ) -> None:
        """Delete a history record."""

        db.delete(history)
        db.commit()

    @staticmethod
    def delete_all_by_user(
        db: Session,
        user_id: int,
    ) -> int:
        """Delete all history records for a user."""

        deleted = (
            db.query(History)
            .filter(History.user_id == user_id)
            .delete()
        )

        db.commit()
        return deleted