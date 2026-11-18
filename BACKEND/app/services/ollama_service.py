"""Service for communicating with the Ollama API."""

import requests


class OllamaService:
    """Handles AI response generation using Ollama."""

    BASE_URL = "http://localhost:11434/api/generate"
    MODEL = "phi3"

    @classmethod
    def generate_response(cls, prompt: str) -> str:
        """Generate a response from the configured Ollama model."""

        payload = {
            "model": cls.MODEL,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                cls.BASE_URL,
                json=payload,
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                "No response generated.",
            )

        except requests.exceptions.RequestException as exc:
            return f"Ollama connection error: {exc}"

        except Exception as exc:
            return f"Unexpected error: {exc}"