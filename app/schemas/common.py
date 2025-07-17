from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class DateMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    
    