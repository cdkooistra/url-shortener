from fastapi import FastAPI
from auth.routes import router as auth_router
from auth.models import create_database

create_database()

app = FastAPI()
app.include_router(auth_router)
