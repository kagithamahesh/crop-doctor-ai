from uuid import UUID
from sqlalchemy.orm import Session

from app.models.corp import Crop
from app.models.farm import Farm
from app.models.user import User
from app.schemas.crop import CropCreate, CropUpdate

def create_crop(
    db: Session,
    crop: CropCreate,
    current_user: User,
):
    farm = (
        db.query(Farm)
        .filter(
            Farm.id == crop.farm_id,
            Farm.owner_id == current_user.id,
        )
        .first()
    )
    if not farm:
        raise ValueError(
            "Farm not found or access denied"
        )
    new_crop = Crop(
        name=crop.name,
        variety=crop.variety,
        season=crop.season,
        farm_id=crop.farm_id,
        )
    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)

    return new_crop

def get_my_crops(
    db: Session,
    current_user: User,
):
    return (
        db.query(Crop)
        .join(Farm)
        .filter(Farm.owner_id == current_user.id)
        .all()
    )

def get_crop_by_id(
    db: Session,
    crop_id: UUID,
    current_user: User,
):
    crop = (
        db.query(Crop)
        .join(Farm)
        .filter(
            Crop.id == crop_id,
            Farm.owner_id == current_user.id,
        )
        .first()
    )

    if not crop:
        raise ValueError("Crop not found")

    return crop


def update_crop(
    db: Session,
    crop_id: UUID,
    crop_data: CropUpdate,
    current_user: User,
):
    crop = get_crop_by_id(
        db,
        crop_id,
        current_user,
    )

    crop.name = crop_data.name
    crop.variety = crop_data.variety
    crop.season = crop_data.season

    db.commit()
    db.refresh(crop)

    return crop

def delete_crop(
    db: Session,
    crop_id: UUID,
    current_user: User,
):
    crop = get_crop_by_id(
        db,
        crop_id,
        current_user,
    )

    db.delete(crop)
    db.commit()

    return {
        "message": "Crop deleted successfully"
    }