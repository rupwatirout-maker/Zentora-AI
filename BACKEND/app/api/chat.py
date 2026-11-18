from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
def send_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if request.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only send messages for your own account.",
        )

    chat = ChatService.send_message(
        db=db,
        user_id=current_user.id,
        message=request.message,
    )

    return ChatResponse(
        id=chat.id,
        user_id=chat.user_id,
        user_message=chat.user_message,
        ai_response=chat.ai_response,
        created_at=chat.created_at,
    )


@router.get("/history/{user_id}")
def get_history(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own chat history.",
        )

    return ChatService.get_chat_history(
        db=db,
        user_id=current_user.id,
    )


@router.delete("/{chat_id}")
def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = ChatService.delete_chat(
        db=db,
        chat_id=chat_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Chat not found.",
        )

    return {
        "message": "Chat deleted successfully.",
    }
