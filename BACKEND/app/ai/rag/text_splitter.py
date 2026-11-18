"""
Text splitting utilities for RAG.
"""

from typing import List


class TextSplitter:
    """Split large text into overlapping chunks."""

    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 100,
    ) -> List[str]:
        """
        Split text into overlapping chunks.
        """

        if not text.strip():
            return []

        chunks = []

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks