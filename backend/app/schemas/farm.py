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

    model_config = {
        "from_attributes": True
    }