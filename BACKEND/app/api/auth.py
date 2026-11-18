from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.auth_schema import UserSignup, UserLogin
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post("/signup")
def signup(
    user: UserSignup,
    db: Session = Depends(get_db),
):
    try:
        new_user = AuthService.signup(db, user)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return {
        "message": "User created successfully",
        "user_id": new_user.id,
        "email": new_user.email,
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        token = AuthService.login(db, user)
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )

    authenticated_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    return {
        "access_token": token["access_token"],
        "token_type": token["token_type"],
        "user": {
            "id": authenticated_user.id,
            "username": authenticated_user.username,
            "email": authenticated_user.email,
        },
    }
