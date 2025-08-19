from fastapi import APIRouter
from app.router.api import user

api_router = APIRouter()

api_router.include_router(user.router)