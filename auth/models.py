from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Field, create_engine, Session
from auth.utils import read_secret
import os

DATABASE_PW = os.getenv("DB_PW")
DATABASE_URL = f"postgresql+psycopg2://postgres_user:{DATABASE_PW}@postgres/database"

engine = create_engine(DATABASE_URL)

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