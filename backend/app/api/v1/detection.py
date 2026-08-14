from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependency import get_db
from app.models.user import User
from app.core.dependencies.roles import require_roles
from app.models.corp import Crop
from app.services.image_service import save_image
from app.models.disease_detection import DiseaseDetection
from app.services.detection_analysis import analyze_detection

router = APIRouter()


@router.post("/upload")
def upload_crop_image(
    crop_id: UUID,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("farmer")),
):
    crop = (
        db.query(Crop)
        .filter(Crop.id == crop_id)
        .first()
    )
    if not crop:
        raise HTTPException(
            status_code=404,
            detail="Crop not found",
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


@router.post("/analyze/{detection_id}")
async def analyze(
    detection_id: str,
    db: Session = Depends(get_db),
):
    try:
        return await analyze_detection(
            db=db,
            detection_id=detection_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )