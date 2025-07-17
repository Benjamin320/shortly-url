from app.crud.user_repository import UserRepository
from app.models.user_model import User

from passlib.context import CryptContext
from datetime import datetime

class UserService():
    def __init__(self, session):
        self.repo = UserRepository(session)
        
    def create_user(self, user: User):
        user_gmail = self.repo.get_user_by_email(user.email)
        
        if user_gmail:
            raise Exception("User already exists")
        
        if not all([user.username, user.email, user.password, user.rol_id]):
            raise Exception("All fields are required")
        
        #! hasheo la contraseña
        user.password = self.hash_password(user.password)
        
        user_created = self.repo.create_user(user)
        
        return user_created
    
    def hash_password(self, password: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_user_by_email(self, email: str):
        return self.repo.get_user_by_email(email).first()
    
    def get_user_by_id(self, user_id: int):
        return self.repo.get_user_by_id(user_id)
    
