"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.profile import router as profile_router
from app.api.upload import router as upload_router
from app.api.settings import router as settings_router
from app.api.admin import router as admin_router
from app.core.config import settings
from app.database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate critical configuration before accepting requests."""

    settings.validate_runtime_config()
    init_db()
    yield


app = FastAPI(
    title="Zentora AI API",
    version="1.0.0",
    description="Backend API for Zentora AI.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(profile_router)
app.include_router(upload_router)
app.include_router(settings_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Velora AI API is running.",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
