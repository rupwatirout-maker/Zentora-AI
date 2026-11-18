"""
==========================================================
File Manager

Why this file exists:
---------------------
This module centralizes every file operation in one place.

Instead of writing file handling logic inside APIs or
Services, we keep everything here.

Benefits:
- Production-ready architecture
- Easy to maintain
- Easy to reuse
- Easy to test
- Automatic file organization

Responsibilities:
- Detect file type
- Create upload folders
- Generate unique filenames
- Save uploaded files
- Delete uploaded files
==========================================================
"""

import os
import shutil
import uuid

from fastapi import UploadFile


class FileManager:
    """
    Centralized File Manager.

    Why?
    ----
    Every upload in the application should go through
    this class instead of handling files inside APIs
    or Services.
    """

    # --------------------------------------------------
    # Base Upload Folder
    #
    # Why?
    # ----
    # Keeping one base folder allows us to organize
    # every uploaded file automatically.
    # --------------------------------------------------

    BASE_UPLOAD_FOLDER = "uploads"

    # --------------------------------------------------
    # Save File
    # --------------------------------------------------

    @staticmethod
    def save_file(upload_file: UploadFile):
        """
        Save an uploaded file.

        Why?
        ----
        Automatically detects the file type and stores it
        inside the correct folder.
        """

        content_type = upload_file.content_type or ""

        # ----------------------------------------------
        # Decide destination folder
        # ----------------------------------------------

        if content_type.startswith("image/"):
            folder = "images"

        elif content_type.startswith("audio/"):
            folder = "audio"

        else:
            folder = "documents"

        upload_dir = os.path.join(
            FileManager.BASE_UPLOAD_FOLDER,
            folder,
        )

        # Create folder if missing
        os.makedirs(upload_dir, exist_ok=True)

        # ----------------------------------------------
        # Generate unique filename
        # ----------------------------------------------

        extension = os.path.splitext(
            upload_file.filename
        )[1]

        unique_filename = (
            f"{uuid.uuid4()}{extension}"
        )

        file_path = os.path.join(
            upload_dir,
            unique_filename,
        )

        # ----------------------------------------------
        # Save physical file
        # ----------------------------------------------

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                upload_file.file,
                buffer,
            )

        # ----------------------------------------------
        # Return metadata
        # ----------------------------------------------

        return {
            "original_filename": upload_file.filename,
            "stored_filename": unique_filename,
            "file_path": file_path,
            "file_type": content_type,
            "file_size": os.path.getsize(file_path),
        }

    # --------------------------------------------------
    # Delete File
    # --------------------------------------------------

    @staticmethod
    def delete_file(file_path: str):
        """
        Delete a physical file.

        Why?
        ----
        Prevent orphan files from remaining on disk.
        """

        if os.path.exists(file_path):
            os.remove(file_path)
            return True

        return False