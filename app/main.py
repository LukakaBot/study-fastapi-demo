from fastapi import FastAPI
from app.router.main import api_router
from app.core.db import create_db_and_tables
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")
