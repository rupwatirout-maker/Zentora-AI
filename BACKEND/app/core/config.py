"""Application configuration and runtime validation."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    AI_PROVIDER: str = "ollama"

    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    OLLAMA_MODEL: str = "phi3"

    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""

    DATABASE_URL: str = "sqlite:///./velora.db"
    CHROMA_DB_PATH: str = "./chroma_db"

    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10

    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174"

    APP_NAME: str = "Velora-AI"
    DEBUG: bool = True

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip().rstrip("/")
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    def validate_runtime_config(self) -> None:
        """Reject unsafe authentication and CORS configuration at startup."""

        if len(self.JWT_SECRET_KEY.strip()) < 32:
            raise RuntimeError(
                "JWT_SECRET_KEY must contain at least 32 characters."
            )

        if self.JWT_ALGORITHM != "HS256":
            raise RuntimeError(
                "JWT_ALGORITHM must be HS256 for the current security setup."
            )

        origins = self.cors_origins

        if not origins or "*" in origins:
            raise RuntimeError(
                "CORS_ORIGINS must contain explicit frontend origins. "
                "Wildcard origins are not allowed."
            )


settings = Settings()