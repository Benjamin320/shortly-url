from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.auth import verify_token, create_acces_token, create_refresh_token, revoke_refresh_token
from app.schemas.user import UserLogin, UserRegister, UserInfo
from app.core.db import db

from app.services.user_services import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login_endpoint(user: UserLogin, db = Depends(db)):
    print(type(db))
    service = UserService(db)
    
    user_db = service.get_user_by_email(user.email)
    
    if not user_db:
        raise Exception("User not found")
    
    if not service.verify_password(user.password, user_db.password):
        raise Exception("Invalid password")
    
    data = UserInfo(username=user_db.username, rol=user_db.rol_id, email=user_db.email)
    
    token = create_acces_token(data)
    refresh_token = create_refresh_token(db, user_db.id)
    
    return {"token": token, "refresh_token": refresh_token} 

@router.post("/create_user")
async def create_user_endpoint(user: UserRegister, db = Depends(db)):
    service = UserService(db)
    try:
        return service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def read_users_me(user = Depends(verify_token)):
    return {"user": user}

@router.post("/logout")
async def logout_endpoint(user = Depends(verify_token), db = Depends(db)):
    user_service = UserService(db)
    
    user_db = user_service.get_user_by_email(user.get("email"))
    
    resp = revoke_refresh_token(user_db.id, db)
    
    if not resp.get("message") or resp.get("message") != "Token revoked":
        raise HTTPException(status_code=500, detail="Error revoking token")
    
    return {"message": "Logout successful"}
    
    