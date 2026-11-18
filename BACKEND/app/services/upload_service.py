"""Business logic for file uploads."""

import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai.rag.rag_service import RAGService
from app.models.uploaded_file import UploadedFile
from app.repositories.upload_repository import UploadRepository

UPLOAD_DIR = "uploads"  # adjust to your actual storage location


class UploadService:
    """Handles uploaded files."""

    @staticmethod
    def upload_file(
        db: Session,
        user_id: int,
        file: UploadFile,
    ) -> UploadedFile:
        """Save the uploaded file to disk, record it, and index it for RAG."""

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Generate a unique name so stored_filename stays unique on disk/DB
        file_extension = os.path.splitext(file.filename)[1]
        stored_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, stored_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(file_path)

        uploaded_file = UploadedFile(
            user_id=user_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_type=file.content_type,
            file_size=file_size,
        )

        created_file = UploadRepository.create(db=db, uploaded_file=uploaded_file)

        # Index the file for retrieval-augmented generation
        RAGService.index_document(
            file_path=created_file.file_path,
            file_id=str(created_file.id),
            user_id=user_id,
        )

        return created_file

    @staticmethod
    def list_files(
        db: Session,
        user_id: int,
    ) -> list[UploadedFile]:
        """Return all files uploaded by a user."""

        return UploadRepository.get_all_by_user(db=db, user_id=user_id)

    @staticmethod
    def delete_file(
        db: Session,
        file_id: int,
    ) -> UploadedFile | None:
        """Delete an uploaded file by ID, its vectors, and its physical file. Returns None if not found."""

        uploaded_file = UploadRepository.get_by_id(db=db, file_id=file_id)

        if uploaded_file is None:
            return None

        # Remove the physical file, if it exists
        if os.path.exists(uploaded_file.file_path):
            os.remove(uploaded_file.file_path)

        # Remove its indexed vectors
        RAGService.delete_document(file_id=str(uploaded_file.id))

        UploadRepository.delete(db=db, uploaded_file=uploaded_file)
        return uploaded_file