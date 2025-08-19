from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL = "postgresql://devuser:devuser@localhost:5432/postgres"

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
