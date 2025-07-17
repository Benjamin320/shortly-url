from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING

from app.schemas.common import DateMixin

if TYPE_CHECKING:
    from app.models.user_model import User

class Rol(DateMixin, SQLModel, table=True):
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=32, unique=True)
    
    users: list['User'] = Relationship(back_populates="rol")
    
    