"""
Gemini provider implementation.
"""

from app.ai.providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):
    """Gemini provider."""

    def generate_response(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "Gemini provider is not implemented yet."
        )