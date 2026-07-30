from uuid import UUID

from sqlalchemy.orm import Session

from app.models.farm import Farm
from app.models.user import User
from app.schemas.farm import FarmUpdate
from app.schemas.farm import FarmCreate


def create_farm(
    db: Session,
    farm: FarmCreate,
    current_user: User,
) -> Farm:

    new_farm = Farm(
        name=farm.name,
        location=farm.location,
        area=farm.area,
        owner_id=current_user.id,
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return new_farm

def get_my_farms(db: Session,
    current_user: User,):
    return (
        db.query(Farm)
        .filter(Farm.owner_id == current_user.id)
        .all()
    )
def get_farm_by_id(db:Session,farm_id: UUID, current_user: User):
    farm=(
        db.query(Farm)
        .filter(
            Farm.id == farm_id,
            Farm.owner_id == current_user.id
            )
        .first()
    )
    if not farm:
        raise ValueError("Farm not found")

    return farm


    
def update_farm(
    db: Session,
    farm_id: UUID,
    farm_data: FarmUpdate,
    current_user: User,
):

    farm = get_farm_by_id(db, farm_id, current_user)

    farm.name = farm_data.name
    farm.location = farm_data.location
    farm.area = farm_data.area

    db.commit()
    db.refresh(farm)

    return farm

def delete_farm(
    db: Session,
    farm_id,
    current_user: User,
):
    farm = (
        db.query(Farm)
        .filter(
            Farm.id == farm_id,
            Farm.owner_id == current_user.id,
        )
        .first()
    )

    if not farm:
        raise ValueError("Farm not found")

    db.delete(farm)
    db.commit()

    return {"message": "Farm deleted successfully"}

def get_farm(
    db: Session,
    farm_id,
    current_user: User,
):
    farm = (
        db.query(Farm)
        .filter(
            Farm.id == farm_id,
            Farm.owner_id == current_user.id,
        )
        .first()
    )

    if not farm:
        raise ValueError("Farm not found")

    return farm