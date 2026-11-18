from fastapi import APIRouter

from app.admin.admin_router import router as admin_router

router = APIRouter(
    tags=["Admin"],
)

router.include_router(admin_router)