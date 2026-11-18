from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile_schema import ProfileResponse, ProfileUpdate
from app.services.profile_service import ProfileService


router = APIRouter(
    prefix="/api/profile",
    tags=["Profile"],
)


def verify_profile_access(user_id: int, current_user: User):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own profile.",
        )


@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_profile_access(user_id, current_user)

    profile = ProfileService.get_profile(
        db=db,
        user_id=user_id,
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    return profile


@router.put("/{user_id}", response_model=ProfileResponse)
def update_profile(
    user_id: int,
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    verify_profile_access(user_id, current_user)

    profile = (
        db.query(Profile)
        .filter(Profile.user_id == user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    return ProfileService.update_profile(
        db=db,
        profile=profile,
        data=data,
    )
