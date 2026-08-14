from uuid import UUID

from fastapi import APIRouter,UploadFile,File,Depends,HTTPException
from sqlalchemy.orm import Session, session

from app.database.dependency import get_db
from app.models.user import User
from app.core.dependencies.roles import require_roles
from app.models.corp import Crop
from app.services.image_service import save_image
from app.models.disease_detection import DiseaseDetection

router = APIRouter()

@router.post("/upload")
def upload_corp_image(
    crop_id: UUID,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    crop=(
        db.query(Crop)
        .filter(Crop.id == crop_id)
        .first()
    )
    if not crop:
        raise HTTPException(
            status_code=404,
            detail="Corp not found",
        )
    image_path = save_image(image)
    detection = DiseaseDetection(
     crop_id = crop.id,
     image_path=image_path,
     location=current_user.farm_location,  
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)

    return {
        "message": "Image uploaded successfully",
        "detection_id": detection.id,
        "image_path": image_path,
    }