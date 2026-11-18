"""
Document processing utilities.
"""

from pathlib import Path

import pymupdf
from docx import Document


class DocumentProcessor:
    """Extract text from supported documents."""

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
    }

    @staticmethod
    def extract_text(
        file_path: str,
    ) -> str:
        """
        Extract text from a supported document.
        """

        path = Path(file_path)

        extension = path.suffix.lower()

        if extension not in DocumentProcessor.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == ".pdf":
            return DocumentProcessor._extract_pdf(
                file_path,
            )

        if extension == ".docx":
            return DocumentProcessor._extract_docx(
                file_path,
            )

        if extension == ".txt":
            return DocumentProcessor._extract_txt(
                file_path,
            )

        return ""

    @staticmethod
    def _extract_pdf(
        file_path: str,
    ) -> str:
        """
        Extract text from a PDF.
        """

        document = pymupdf.open(file_path)

        text = []

        for page in document:
            page_text = page.get_text()

            if page_text:
                text.append(page_text)

        document.close()

        return "\n".join(text)

    @staticmethod
    def _extract_docx(
        file_path: str,
    ) -> str:
        """
        Extract text from a DOCX file.
        """

        document = Document(file_path)

        text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)

    @staticmethod
    def _extract_txt(
        file_path: str,
    ) -> str:
        """
        Extract text from a TXT file.
        """

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            return file.read()