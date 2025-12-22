from typing import Annotated,Optional
from sqlmodel import Session,SQLModel,create_engine
from fastapi import Depends

sqlite_filename = "database.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session_generator():
    with Session(engine) as session:
        yield session

def get_session():
    with Session(engine) as session:
        return session
    
SessionDep = Annotated[Session, Depends(get_session_generator)]


    