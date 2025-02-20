from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select, Integer, delete
from app.utils import read_secret

DATABASE_PW = read_secret("db_pw")
DATABASE_URL = f"postgresql+psycopg2://postgres_user:{DATABASE_PW}@postgres/database"

engine = create_engine(DATABASE_URL)

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

