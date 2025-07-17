from sqlmodel import SQLModel, Field
from datetime import datetime

class TokenUpdate(SQLModel):
    update_at: datetime = Field(default_factory=datetime.now)

class TokenExpiration(TokenUpdate):
    expiration: datetime
    refresh_token: str
    user_id: int