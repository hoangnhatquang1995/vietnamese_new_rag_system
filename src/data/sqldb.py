from typing import Annotated, Optional
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends

BASE_DIR = Path(__file__).resolve().parents[2]
SQLITE_PATH = (BASE_DIR / "database.db").resolve()
sqlite_url = f"sqlite:///{SQLITE_PATH.as_posix()}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)

def get_session_generator():
    with Session(engine) as session:
        yield session

def get_session():
    with Session(engine) as session:
        return session
    
SessionDep = Annotated[Session, Depends(get_session_generator)]
    