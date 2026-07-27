from fastapi import APIRouter, UploadFile, File, Depends
from app.models.user import User
from app.core.dependencies.roles import require_roles

router = APIRouter()


@router.post("/upload")
async def upload_crop(
    image: UploadFile = File(...),
    current_user: User = Depends(
        require_roles("farmer")
    ),
):
    return {
        "filename": image.filename,
        "content_type": image.content_type,
        "uploaded_by": current_user.email,
    }