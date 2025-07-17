from fastapi import APIRouter

from app.api.routes import user_router, token_router

router = APIRouter()

router.include_router(user_router.router)
router.include_router(token_router.router)