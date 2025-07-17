from sqlmodel import select, Session

from app.models.user_model import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_user(self, user: User):
        userModel = User(
            username=user.username,
            email=user.email,
            password=user.password
        )
        
        self.session.add(userModel)
        self.session.commit()
        self.session.refresh(userModel)
        return userModel
    
    def get_user_by_email(self, email:str):
        
        users = self.session.exec(select(User).where(User.email == email))
        
        return users
    
    def get_user_by_id(self, user_id:int):
        
        user = self.session.exec(select(User).where(User.id == user_id)).first()
        
        return user
    
    
    
        