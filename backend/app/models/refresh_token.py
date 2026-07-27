from datetime  import datetime

from sqlalchemy import DateTime,ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.models.basemodel import BaseModel

class RefreshToken(BaseModel):
    __tablename__="refresh_tokens"

    token : Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    revoked: Mapped[bool] = mapped_column(
        default=False,
    )

    user = relationship("User")