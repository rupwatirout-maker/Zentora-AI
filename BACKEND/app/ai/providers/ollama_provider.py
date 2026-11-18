"""
Ollama AI provider implementation.
"""

import requests

from app.ai.providers.base_provider import BaseProvider
from app.core.config import settings


class OllamaProvider(BaseProvider):
    """AI provider for Ollama."""

    def __init__(self):
        """Initialize Ollama configuration from settings."""

        self.model = settings.OLLAMA_MODEL
        self.url = settings.OLLAMA_URL

    def generate_response(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response using Ollama.
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                "No response generated.",
            )

        except requests.RequestException as exc:
            return f"Ollama Error: {exc}"