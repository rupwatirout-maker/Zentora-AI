"""
Vector store using ChromaDB.
"""

import chromadb

from app.core.config import settings


class VectorStore:
    """Handles vector storage and retrieval."""

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
        )

        self.collection = self.client.get_or_create_collection(
            name="velora_documents",
        )

    def add_documents(
        self,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        """
        Store documents in ChromaDB.
        """

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[str]:
        """
        Retrieve relevant documents.
        """

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        documents = results.get(
            "documents",
            [],
        )

        if not documents:
            return []

        return documents[0]

    def delete_by_file(
        self,
        file_id: str,
    ) -> None:
        """
        Delete all vectors belonging to a file.
        """

        self.collection.delete(
            where={
                "file_id": file_id,
            },
        )