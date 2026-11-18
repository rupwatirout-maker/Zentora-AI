"""Business logic for chat history."""

from sqlalchemy.orm import Session

from app.models.history import History
from app.repositories.history_repository import HistoryRepository


class HistoryService:
    """Handles chat history operations."""

    @staticmethod
    def create_history(
        db: Session,
        user_id: int,
        user_message: str,
        ai_response: str,
    ) -> History:
        """Create a history record."""

        history = History(
            user_id=user_id,
            user_message=user_message,
            ai_response=ai_response,
        )

        return HistoryRepository.create(
            db=db,
            history=history,
        )

    @staticmethod
    def get_history(
        db: Session,
        user_id: int,
    ):
        """Return a user's chat history."""

        return HistoryRepository.get_all_by_user(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def delete_history(
        db: Session,
        history_id: int,
    ) -> bool:
        """Delete a history record."""

        history = HistoryRepository.get_by_id(
            db=db,
            history_id=history_id,
        )

        if history is None:
            return False

        HistoryRepository.delete(
            db=db,
            history=history,
        )

        return True

    @staticmethod
    def clear_history(
        db: Session,
        user_id: int,
    ) -> int:
        """Delete all history for a user."""

        return HistoryRepository.delete_all_by_user(
            db=db,
            user_id=user_id,
        )