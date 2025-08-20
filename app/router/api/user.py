from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Field
from datetime import datetime
from app.core.db import SessionDep
from sqlmodel import select
from pydantic import BaseModel


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


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login_user(login_request: LoginRequest, session: SessionDep):
    # 查询用户
    statement = select(Users).where(
        Users.username == login_request.username, Users.is_deleted == False
    )
    user = session.exec(statement).first()

    # 检查用户是否存在
    if not user:
        return JSONResponse(content={"code": 400, "msg": "用户不存在", "data": None})

    # 验证密码
    if user.password != login_request.password:
        return JSONResponse(content={"code": 400, "msg": "密码错误", "data": None})

    # 登录成功
    return JSONResponse(
        content={
            "code": 200,
            "msg": "登录成功",
            "data": user.model_dump(mode="json"),
        }
    )


@router.get("/user")
def get_user(id: int, session: SessionDep):
    statement = select(Users).where(Users.user_id == id, Users.is_deleted == False)
    result = session.exec(statement).first()
    if result:
        return JSONResponse(
            content={
                "code": 200,
                "msg": "success",
                "data": result.model_dump(mode="json"),
            }
        )
    else:
        return JSONResponse(content={"code": 400, "msg": "用户不存在", "data": None})


@router.post("/user")
def create_user(user: Users, session: SessionDep):
    # 检查用户名是否已存在
    statement = select(Users).where(Users.username == user.username)
    result = session.exec(statement).first()
    if result:
        return JSONResponse(
            content={"code": 400, "msg": "用户名已存在，请勿重复创建", "data": None}
        )

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return JSONResponse(
            content={
                "code": 200,
                "msg": "success",
                "data": user.model_dump(mode="json"),
            }
        )
    except Exception as e:
        print(e)
        return JSONResponse(content={"code": 500, "msg": str(e), "data": None})


@router.put("/user")
def update_user(user: Users, session: SessionDep):
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return JSONResponse(
            content={
                "code": 200,
                "msg": "success",
                "data": user.model_dump(mode="json"),
            }
        )
    except Exception as e:
        print(e)
        return JSONResponse(content={"code": 500, "msg": str(e), "data": None})


@router.delete("/user")
def delete_user(id: int, session: SessionDep):
    try:
        statement = select(Users).where(Users.user_id == id)
        result = session.exec(statement).first()
        if result:
            result.is_deleted = True
            result.updated_at = datetime.now()
            session.add(result)
            session.commit()
            return JSONResponse(
                content={
                    "code": 200,
                    "msg": "success",
                    "data": None,
                }
            )
        else:
            return JSONResponse(
                content={"code": 400, "msg": "用户不存在", "data": None}
            )
    except Exception as e:
        print(e)
        return JSONResponse(content={"code": 500, "msg": str(e), "data": None})
