from fastapi import APIRouter, Depends
from requests import Session

from app.database.dependency import get_db


router = APIRouter()

@router.get("/health")
def health(db: Session = Depends(get_db)):
    return {
        "status": "healthy",
        "message": "Crop Doctor AI Backend Running"
    }
    