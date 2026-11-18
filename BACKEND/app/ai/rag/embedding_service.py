"""
Embedding service for RAG.
"""

from typing import List

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Generates vector embeddings."""

    _model = None

    @classmethod
    def get_model(cls):
        """Load the embedding model only once."""

        if cls._model is None:
            cls._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

        return cls._model

    @classmethod
    def embed_text(
        cls,
        text: str,
    ) -> List[float]:
        """
        Generate an embedding for a single text.
        """

        model = cls.get_model()

        embedding = model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    @classmethod
    def embed_documents(
        cls,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.
        """

        model = cls.get_model()

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    @classmethod
    def embed_query(
        cls,
        query: str,
    ) -> List[float]:
        """
        Generate an embedding for a search query.
        """

        model = cls.get_model()

        embedding = model.encode(
            query,
            normalize_embeddings=True,
        )

        return embedding.tolist()