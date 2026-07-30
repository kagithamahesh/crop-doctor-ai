from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.dependencies.roles import require_roles
from app.schemas.crop import CropCreate, CropResponse, CropUpdate
from app.database.dependency import get_db
from app.services.crop_service import create_crop, delete_crop, get_crop_by_id, get_my_crops, update_crop

router = APIRouter()


@router.post(
    "/",
    response_model=CropResponse,
)
def add_crop(
    crop: CropCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("farmer")
    ),
):
    try:
        return create_crop(
            db,
            crop,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
@router.get(
    "/",
    response_model=List[CropResponse],
)
def list_crops(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    return get_my_crops(
        db,
        current_user,
    )


@router.get(
    "/{crop_id}",
    response_model=CropResponse,
)
def get_crop(
    crop_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    try:
        return get_crop_by_id(
            db,
            crop_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.put(
    "/{crop_id}",
    response_model=CropResponse,
)
def edit_crop(
    crop_id: UUID,
    crop: CropUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    try:
        return update_crop(
            db,
            crop_id,
            crop,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete("/{crop_id}")
def remove_crop(
    crop_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    try:
        return delete_crop(
            db,
            crop_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )