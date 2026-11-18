"""Database model for user profiles."""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Profile(Base):
    """Stores additional user profile information."""

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    full_name = Column(
        String,
        nullable=True,
    )

    phone = Column(
        String,
        nullable=True,
    )

    bio = Column(
        String,
        nullable=True,
    )

    avatar = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # User relationship
    user = relationship(
        "User",
        back_populates="profile",
    )