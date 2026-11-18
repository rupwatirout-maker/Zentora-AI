"""
OpenAI provider implementation.
"""

from app.ai.providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI provider."""

    def generate_response(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "OpenAI provider is not implemented yet."
        )