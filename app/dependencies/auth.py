from fastapi import Depends, HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from sqlmodel import Session

from app.core.config import settings
from app.core.db import db
from app.schemas.user import UserInfo
from app.services.token_services import TokenServices
from app.models.token_refresh_model import TokenRefresh
from app.schemas.token_refresh import TokenExpiration

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


#! Funcion de ayuda para crear los jwt en las demas funciones
def create_jwt(expiration: timedelta, type_token: str = "access", sub: int = None, username: str = None, rol: int = None, email: str = None) -> str:
    
    if type_token == "access":
        to_encode = {"username": username, "rol": rol, "email": email, "exp": datetime.now(timezone.utc) + expiration, "type": "access"}
        
        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        return token
    elif type_token == "refresh":
        to_encode = {"sub": sub, "exp": datetime.now(timezone.utc) + expiration, "type": "refresh"}
        
        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        return token

#* crear token
def create_acces_token(data: UserInfo, expiration: timedelta = timedelta(minutes=15)):
    to_encode = data.model_dump()
    print(to_encode)    
    
    token = create_jwt(
        expiration=expiration, 
        type_token="access", 
        username=to_encode["username"], 
        rol=to_encode["rol"], 
        email=to_encode["email"]
    )
    
    return token

#* crear refresh token	
def create_refresh_token(db: Session, user_id: int, expiration: timedelta = timedelta(days=7)):
    tokenService = TokenServices(db)
    expire_at = datetime.now(timezone.utc) + expiration
    
    try:
        refresh_token_db = tokenService.get_token_by_id(user_id)
        
        #* Si el refresh token ya existe, lo actualizaremos
        if refresh_token_db is not None:
            refresh_token = create_jwt(
                expiration=expiration, 
                type_token="refresh", 
                sub=user_id
            )
            
            token_u = TokenExpiration(
                expiration=expire_at, 
                user_id=user_id,
                refresh_token=refresh_token
            )
            
            tokenService.update_expiration_token(token_u)
            
            return refresh_token
        
        #* Si el refresh token no existe o esta expirado, creamos otro
        refresh_token = create_jwt(
            expiration=expiration, 
            type_token="refresh", 
            sub=user_id
        )

        token_create = tokenService.create_token(TokenRefresh(refresh_token=refresh_token, user_id=user_id))

        if token_create is None:
            raise HTTPException(status_code=500, detail="Error al crear el token")

        return refresh_token
    except JWTError as e:
        raise HTTPException(status_code=500, detail=str(e))

#* verificar token
def verify_token(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        #! Verifica que el token tenga los datos necesarios
        if not all([payload.get('username'), payload.get('rol'), payload.get('email')]):
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        #! Verifica que el token sea de tipo access
        if payload["type"] != "access":
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        return payload
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    

def verify_refresh_token(db: Session = Depends(db), token: str = Depends(oauth2_scheme)):
    tokenService = TokenServices(db)
    try:    
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        token_db = tokenService.get_token_by_id(payload["sub"])
        
        if token_db is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        if token_db.refresh_token != token:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        #! Verifica que el token tenga los datos necesarios
        if not all(payload.get('sub')):
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        #! Verifica que el token sea de tipo refresh
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        return payload
        
    except ExpiredSignatureError:
        
        #! Si el token expira, revocaremos el token de la base de datos modificando su state a False
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_db = tokenService.get_token_by_id(payload["sub"])
        if token_db:
            tokenService.delete_token(token_db.id)
            raise HTTPException(status_code=401, detail="Token expired")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    
def revoke_refresh_token(user_token: int, db: Session = Depends(db)):
    try:
        token_service = TokenServices(db)    
        token_refresh = token_service.get_token_by_id(user_token)
    
        if token_refresh is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        token_service.delete_token(token_refresh.id)
        
        return {"message": "Token revoked"}
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")