from sqlmodel import select, Session
from fastapi import HTTPException
from datetime import datetime

from app.models.token_refresh_model import TokenRefresh
from app.schemas.token_refresh import TokenExpiration

class TokenRefreshRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def create_token(self, token: TokenRefresh):
        tokenModel = TokenRefresh(
            refresh_token=token.refresh_token,
            user_id=token.user_id
        )
        
        self.session.add(tokenModel)
        self.session.commit()
        self.session.refresh(tokenModel)
        return tokenModel
    
    def get_token_by_user_id(self, user_id: int):
        try:
            token = self.session.exec(select(TokenRefresh).where(TokenRefresh.user_id == user_id).where(TokenRefresh.state == True)).first()
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_token_by_id(self, token_id: int):
        try:
            token = self.session.exec(select(TokenRefresh).where(TokenRefresh.id == token_id).where(TokenRefresh.state == True)).first()
            
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def update_expiration(self, token_upd: TokenExpiration):
        try:
            token = self.get_token_by_user_id(token_upd.user_id)
            token.expiration = token_upd.expiration
            token.updated_at = token_upd.update_at
            token.refresh_token = token_upd.refresh_token
            self.session.commit()
            
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def revoke_token(self, token_id: int):
        try:
            token = self.get_token_by_id(token_id)
            token.state = False
            token.deleted_at = datetime.now()
            self.session.commit()
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))