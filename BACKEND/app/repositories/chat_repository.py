"""Database operations for chat messages."""

from sqlalchemy.orm import Session

from app.models.chat import Chat


class ChatRepository:
    """Handles chat database queries."""

    @staticmethod
    def create(db: Session, chat: Chat) -> Chat:
        """Create a chat record."""

        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    @staticmethod
    def get_by_id(db: Session, chat_id: int) -> Chat | None:
        """Return a chat by ID."""

        return (
            db.query(Chat)
            .filter(Chat.id == chat_id)
            .first()
        )

    @staticmethod
    def get_all_by_user(db: Session, user_id: int):
        """Return all chats for a user."""

        return (
            db.query(Chat)
            .filter(Chat.user_id == user_id)
            .order_by(Chat.created_at.desc())
            .all()
        )

    @staticmethod
    def delete(db: Session, chat: Chat) -> None:
        """Delete a chat."""

        db.delete(chat)
        db.commit()

    @staticmethod
    def delete_all_by_user(db: Session, user_id: int) -> int:
        """Delete all chats for a user."""

        deleted = (
            db.query(Chat)
            .filter(Chat.user_id == user_id)
            .delete()
        )

        db.commit()
        return deleted