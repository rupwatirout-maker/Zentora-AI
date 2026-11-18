"""Database operations for uploaded files."""

from sqlalchemy.orm import Session

from app.models.uploaded_file import UploadedFile


class UploadRepository:
    """Handles uploaded file database queries."""

    @staticmethod
    def create(db: Session, uploaded_file: UploadedFile) -> UploadedFile:
        """Create a file record."""

        db.add(uploaded_file)
        db.commit()
        db.refresh(uploaded_file)
        return uploaded_file

    @staticmethod
    def get_by_id(db: Session, file_id: int) -> UploadedFile | None:
        """Return a file by ID."""

        return (
            db.query(UploadedFile)
            .filter(UploadedFile.id == file_id)
            .first()
        )

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int,
    ):
        """Return all files uploaded by a user."""

        return (
            db.query(UploadedFile)
            .filter(UploadedFile.user_id == user_id)
            .order_by(UploadedFile.created_at.desc())
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        uploaded_file: UploadedFile,
    ) -> UploadedFile:
        """Persist file changes."""

        db.commit()
        db.refresh(uploaded_file)
        return uploaded_file

    @staticmethod
    def delete(
        db: Session,
        uploaded_file: UploadedFile,
    ) -> None:
        """Delete a file record."""

        db.delete(uploaded_file)
        db.commit()