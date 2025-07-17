from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING

from app.schemas.common import DateMixin

if TYPE_CHECKING:
    from app.models.rol_model import Rol
    from app.models.token_refresh_model import TokenRefresh

class User(DateMixin, SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(max_length=32)
    email: str = Field(max_length=64, unique=True)
    password: str
    rol_id: int = Field(default=1, foreign_key="rol.id")
    
    rol: "Rol" = Relationship(back_populates="users")
    token_refresh: List["TokenRefresh"] = Relationship(back_populates="user")