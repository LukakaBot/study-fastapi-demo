from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Field
from datetime import datetime
from app.core.db import SessionDep
from sqlmodel import select


class Users(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    phone: str = Field(unique=True)
    password: str
    real_name: str = Field(default="")
    is_enabled: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = Field(default=False)


router = APIRouter(tags=["user"])


@router.get("/user")
def get_user():
    return {"name": "Hello World"}


@router.post("/user")
def create_user(user: Users, session: SessionDep):
    # 检查用户名是否已存在
    statement = select(Users).where(Users.username == user.username)
    result = session.exec(statement).first()
    if result:
        return JSONResponse(content={"code": 400, "msg": "用户名已存在，请勿重复创建", "data": None})
    
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return JSONResponse(content={"code": 200, "msg": "success", "data": user.model_dump(mode='json')})
    except Exception as e:
        print(e)
        return JSONResponse(content={"code": 500, "msg": str(e), "data": None})
