from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select, Integer, delete

sqlite_db = f"sqlite:///database.db"

# check_same_thread: False is required to allow FastAPI to use the same db in different threads
engine = create_engine(sqlite_db, connect_args={"check_same_thread": False})

def create_database():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

# do this to avoid having to 'with open' statements in each route definition
SessionDep = Annotated[Session, Depends(get_session)]

class URLModel(SQLModel, table=True):
    url: str = Field(primary_key=True, index=True)
    value: str = Field(index=True)
    username: str= Field(index=True) # Track users and their urls

