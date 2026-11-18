"""
Base interface for all AI providers.
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Abstract base class for every AI provider.

    Every provider (Ollama, OpenAI, Gemini,
    Groq, Claude, etc.) must inherit this class.
    """

    @abstractmethod
    def generate_response(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an AI response.

        Args:
            prompt: User prompt.

        Returns:
            AI generated response.
        """

        raise NotImplementedError(
            "Provider must implement generate_response()."
        )