"""Administrator-only API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.admin.admin_service import AdminService
from app.core.dependencies import get_current_user, require_admin
from app.database.database import get_db
from app.models.user import User
from app.schemas.admin_schema import AdminUserResponse


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    """Return dashboard statistics."""

    return AdminService.get_dashboard(db)


@router.get(
    "/users",
    response_model=list[AdminUserResponse],
)
def get_users(db: Session = Depends(get_db)):
    """Return user information without password hashes."""

    return AdminService.get_all_users(db)


@router.get(
    "/users/{user_id}",
    response_model=AdminUserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """Return a user by ID without sensitive authentication fields."""

    user = AdminService.get_user(db=db, user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a user while enforcing administrator safety rules."""

    try:
        deleted = AdminService.delete_user(
            db=db,
            user_id=user_id,
            actor_user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return {"message": "User deleted successfully."}


@router.get("/system")
def system_info():
    """Return non-sensitive backend system information."""

    return AdminService.get_system_info()
