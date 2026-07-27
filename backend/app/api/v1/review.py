from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies.roles import require_roles

router = APIRouter()


@router.post("/review")
def review_crop(
    crop_id: str,
    disease: str,
    recommendation: str,
    current_user: User = Depends(
        require_roles("agronomist")
    ),
):
    return {
        "crop_id": crop_id,
        "disease": disease,
        "recommendation": recommendation,
        "reviewed_by": current_user.email,
    }