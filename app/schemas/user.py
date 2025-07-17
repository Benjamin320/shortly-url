from sqlmodel import SQLModel, Field

class UserInfo(SQLModel):
    username: str
    rol: int
    email: str
    
class UserLogin(SQLModel):
    email: str
    password: str

class UserRegister(SQLModel):
    username: str
    email: str
    password: str
    rol_id: int = Field(default=1)