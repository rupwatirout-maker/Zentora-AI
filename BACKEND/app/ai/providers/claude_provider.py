"""
Claude provider implementation.
"""

from app.ai.providers.base_provider import BaseProvider


class ClaudeProvider(BaseProvider):
    """Claude provider."""

    def generate_response(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "Claude provider is not implemented yet."
        )