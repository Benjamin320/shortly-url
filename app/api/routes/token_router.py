from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.dependencies.auth import verify_refresh_token, create_acces_token
from app.core.db import db
from app.services.user_services import UserService
from app.schemas.user import UserInfo


router = APIRouter(
    prefix="/token",
    tags=["token"],
    responses={404: {"description": "Not found"}},
)

#* Endpoint para obtener un nuevo access token
@router.get("/refresh")
async def refresh_token_endpoint(token_refresh: str = Depends(verify_refresh_token), db: Session = Depends(db)):
    user_service = UserService(db)
    
    user = user_service.get_user_by_id(token_refresh.get("sub"))
    
    data = UserInfo(username=user.username, rol=user.rol_id, email=user.email)
    
    acces_token = create_acces_token(data)
    
    return {"token": acces_token, "type": "access"}