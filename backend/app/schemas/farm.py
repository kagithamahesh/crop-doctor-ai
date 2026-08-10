from pydantic import BaseModel
from uuid import UUID


class FarmCreate(BaseModel):
    name: str
    location: str
    area: float


class FarmResponse(BaseModel):
    id: UUID
    name: str
    location: str
    area: float
    owner_id: UUID
    model_config = {
        "from_attributes": True
    }

class FarmUpdate(BaseModel):
    name: str
    location: str
    area: float