from fastapi import APIRouter

router = APIRouter(tags=["user"])

@router.get("/user")
def get_user():
    return {"name": "Hello World"}