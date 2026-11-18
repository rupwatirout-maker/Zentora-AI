from sqlalchemy.orm import Session

from app.ai.agents.agent_manager import AgentManager
from app.models.chat import Chat
from app.repositories.chat_repository import ChatRepository


class ChatService:

    @staticmethod
    def send_message(
        db: Session,
        user_id: int,
        message: str,
    ) -> Chat:

        ai_response = AgentManager.generate_response(
            user_id=user_id,
            message=message,
        )

        chat = Chat(
            user_id=user_id,
            user_message=message,
            ai_response=ai_response,
        )

        return ChatRepository.create(
            db=db,
            chat=chat,
        )

    @staticmethod
    def get_chat(
        db: Session,
        chat_id: int,
    ) -> Chat | None:

        return ChatRepository.get_by_id(
            db=db,
            chat_id=chat_id,
        )

    @staticmethod
    def get_chat_history(
        db: Session,
        user_id: int,
    ):

        return ChatRepository.get_all_by_user(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def delete_chat(
        db: Session,
        chat_id: int,
        user_id: int,
    ) -> bool:

        chat = ChatRepository.get_by_id(
            db=db,
            chat_id=chat_id,
        )

        if chat is None:
            return False

        if chat.user_id != user_id:
            return False

        ChatRepository.delete(
            db=db,
            chat=chat,
        )

        return True

    @staticmethod
    def clear_chat_history(
        db: Session,
        user_id: int,
    ) -> int:

        return ChatRepository.delete_all_by_user(
            db=db,
            user_id=user_id,
        )
