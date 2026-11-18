"""Database model for application users."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    """Stores application user accounts and authorization roles."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(150), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)

    # The role column already exists in the current SQLite database.
    role = Column(String(20), nullable=False, default="user", server_default="user")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    profile = relationship(
        "Profile", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
    )
    settings = relationship(
        "Settings", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
    )
    chats = relationship(
        "Chat", back_populates="user", cascade="all, delete-orphan",
    )
    uploaded_files = relationship(
        "UploadedFile", back_populates="user",
        cascade="all, delete-orphan",
    )
    history = relationship(
        "History", back_populates="user", cascade="all, delete-orphan",
    )