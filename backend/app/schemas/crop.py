from pydantic import BaseModel
from uuid import UUID


class CropCreate(BaseModel):
    name: str
    variety: str
    season: str
    farm_id: UUID


class CropResponse(BaseModel):
    id: UUID
    name: str
    variety: str
    season: str

    model_config = {
        "from_attributes": True
    }