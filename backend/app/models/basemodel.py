import uuid
from sqlalchemy import DateTime, func
from app.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

class BaseModel(Base):
    __abstract__ = True
    id :Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[DateTime] = mapped_column(
         DateTime(timezone=True),
         server_default=func.now(),
         onupdate=func.now(),
    )