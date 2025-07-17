from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from app.schemas.common import DateMixin
from app.dependencies.utils import create_expiration
if TYPE_CHECKING:
    from app.models.user_model import User

class TokenRefresh(DateMixin, SQLModel, table=True):
    id: int = Field(primary_key=True)
    refresh_token: str
    deleted_at: Optional[datetime] = Field(default=None, nullable=True) #datetime = None
    user_id: int = Field(foreign_key="user.id")
    expiration: datetime = Field(default_factory=lambda: create_expiration(7), nullable=False)
    state: bool = Field(default=True)
    
    user: "User" = Relationship(back_populates="token_refresh")