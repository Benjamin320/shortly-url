from app.crud.token_repository import TokenRefreshRepository
from app.models.token_refresh_model import TokenRefresh
from app.schemas.token_refresh import TokenExpiration

from datetime import datetime


class TokenServices:
    def __init__(self, session):
        self.repo = TokenRefreshRepository(session)
        
    def create_token(self, token: TokenRefresh):
        return self.repo.create_token(token)
    
    def get_token_by_id(self, user_id: int):
        return self.repo.get_token_by_user_id(user_id)
    
    def get_token(self, token_id: int):
        return self.repo.get_token_by_id(token_id)
    
    def update_expiration_token(self, token_upd: TokenExpiration):
        return self.repo.update_expiration(token_upd)
    
    def delete_token(self, token_id: int):
        return self.repo.revoke_token(token_id)