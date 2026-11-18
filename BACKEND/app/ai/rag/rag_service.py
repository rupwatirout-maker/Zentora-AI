"""
RAG service.
"""

import uuid

from app.ai.rag.document_processor import DocumentProcessor
from app.ai.rag.embedding_service import EmbeddingService
from app.ai.rag.text_splitter import TextSplitter
from app.ai.rag.vector_store import VectorStore


class RAGService:
    """Handles document indexing and retrieval."""

    _vector_store = VectorStore()

    @classmethod
    def index_document(
        cls,
        file_path: str,
        file_id: str,
        user_id: int,
    ) -> None:
        """
        Extract, split, embed and store a document.
        """

        text = DocumentProcessor.extract_text(
            file_path,
        )

        chunks = TextSplitter.split_text(
            text=text,
        )

        if not chunks:
            return

        embeddings = EmbeddingService.embed_documents(
            chunks,
        )

        ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]

        metadatas = [
            {
                "file_id": file_id,
                "user_id": str(user_id),
            }
            for _ in chunks
        ]

        cls._vector_store.add_documents(
            ids=ids,
            texts=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    @classmethod
    def retrieve_context(
        cls,
        query: str,
        top_k: int = 5,
    ) -> str:
        """
        Retrieve relevant document context.
        """

        embedding = EmbeddingService.embed_query(
            query,
        )

        documents = cls._vector_store.search(
            embedding=embedding,
            top_k=top_k,
        )

        return "\n\n".join(documents)

    @classmethod
    def delete_document(
        cls,
        file_id: str,
    ) -> None:
        """
        Remove a document from the vector database.
        """

        cls._vector_store.delete_by_file(
            file_id=file_id,
        )