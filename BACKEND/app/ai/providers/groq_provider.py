"""
Groq provider implementation.
"""

from app.ai.providers.base_provider import BaseProvider


class GroqProvider(BaseProvider):
    """Groq provider."""

    def generate_response(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "Groq provider is not implemented yet."
        )