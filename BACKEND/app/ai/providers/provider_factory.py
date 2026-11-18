from app.ai.providers.ollama_provider import OllamaProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.claude_provider import ClaudeProvider


class ProviderFactory:

    @staticmethod
    def get_provider(provider: str):
        provider = provider.lower().strip()

        if provider == "ollama":
            return OllamaProvider()

        if provider == "openai":
            return OpenAIProvider()

        if provider == "gemini":
            return GeminiProvider()

        if provider == "groq":
            return GroqProvider()

        if provider == "claude":
            return ClaudeProvider()

        raise ValueError(
            f"Unsupported AI provider: {provider}"
        )
