from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.dependency import get_db
from app.schemas.farm import FarmCreate, FarmResponse,FarmUpdate
from app.services.farm_service import create_farm,get_farm_by_id,delete_farm,update_farm,get_my_farms

from app.core.dependencies.auth import get_current_user
from app.core.dependencies.roles import require_roles

from app.models.user import User

router = APIRouter()

@router.get("/{farm_id}",response_model=FarmResponse)
def get_farm(
    farm_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    try:
        return get_farm_by_id(db, farm_id, current_user)
    except  ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.get("/",response_model=List[FarmResponse])
def list_farms(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer"))):
     return get_my_farms(db, current_user)


@router.post(
    "/",
    response_model=FarmResponse,
    status_code=201,
)
def add_farm(
    farm: FarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("farmer")
    ),
):
    try:
        return create_farm(
            db=db,
            farm=farm,
            current_user=current_user,
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.put(
    "/{farm_id}",
    response_model=FarmResponse,
)
def edit_farm(
    farm_id: UUID,
    farm: FarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    try:
        return update_farm(
            db,
            farm_id,
            farm,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    
@router.delete("/{farm_id}")
def remove_farm(
    farm_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    try:
        return delete_farm(
            db,
            farm_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )