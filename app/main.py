from fastapi import FastAPI

from app.core.config import settings
from app.core.db import database
from contextlib import asynccontextmanager

from app.api.main import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = FastAPI(
    title="shortly-url",
    version=settings.VERSION,
    lifespan=lifespan
)


app.include_router(router)