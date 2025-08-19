from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL = "postgresql://devuser:devuser@localhost:5432/postgres"

engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # 连接池大小
    max_overflow=20,     # 超出pool_size后最多创建的连接数
    pool_pre_ping=True,  # 检查连接是否有效
    pool_recycle=3600,   # 连接回收时间（秒）
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session)]
