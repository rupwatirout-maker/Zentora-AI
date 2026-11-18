"""Authentication business logic."""

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth_schema import UserLogin, UserSignup


class AuthService:
    """Handles registration and login."""

    @staticmethod
    def signup(db: Session, user_data: UserSignup):
        existing_user = (
            db.query(User)
            .filter(
                (User.email == user_data.email)
                | (User.username == user_data.username)
            )
            .first()
        )

        if existing_user:
            raise ValueError("Email or username already registered.")

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            role="user",
            is_active=True,
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception:
            db.rollback()
            raise

        return new_user

    @staticmethod
    def login(db: Session, user_data: UserLogin):
        user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if not user or not user.is_active:
            raise ValueError("Invalid credentials.")

        if not verify_password(user_data.password, user.hashed_password):
            raise ValueError("Invalid credentials.")

        access_token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }