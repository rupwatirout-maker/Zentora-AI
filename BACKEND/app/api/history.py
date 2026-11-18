"""API endpoints for chat history."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/api/history",
    tags=["History"],
)


@router.get("/{user_id}")
def get_history(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Return a user's chat history."""

    return ChatService.get_chat_history(
        db=db,
        user_id=user_id,
    )


@router.delete("/{chat_id}")
def delete_history(
    chat_id: int,
    db: Session = Depends(get_db),
):
    """Delete a chat history record."""

    deleted = ChatService.delete_chat(
        db=db,
        chat_id=chat_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Chat not found.",
        )

    return {
        "message": "History deleted successfully.",
    }


@router.delete("/user/{user_id}")
def clear_history(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Delete all chat history for a user."""

    deleted = ChatService.clear_chat_history(
        db=db,
        user_id=user_id,
    )

    return {
        "deleted_records": deleted,
    }