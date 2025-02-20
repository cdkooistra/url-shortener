from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Field, create_engine, Session

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

class UserModel(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    password_hash: str  # Store hashed passwords   