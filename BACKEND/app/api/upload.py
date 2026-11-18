from fastapi import APIRouter, Depends, File, UploadFile, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.upload_schema import UploadResponse
from app.services.upload_service import UploadService


router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"],
)


@router.post(
    "/",
    response_model=UploadResponse,
    summary="Upload File",
    description="Upload a file.",
)
def upload_file(
    user_id: int = Query(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only upload files for your own account.",
        )

    return UploadService.upload_file(
        db=db,
        user_id=current_user.id,
        file=file,
    )


@router.get(
    "/{user_id}",
    response_model=list[UploadResponse],
    summary="List User Files",
)
def list_files(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own files.",
        )

    return UploadService.list_files(
        db=db,
        user_id=current_user.id,
    )


@router.delete(
    "/{file_id}",
    summary="Delete File",
)
def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = UploadService.delete_file(
        db=db,
        file_id=file_id,
        user_id=current_user.id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return {
        "message": "File deleted successfully."
    }
