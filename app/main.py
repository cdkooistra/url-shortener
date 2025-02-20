from fastapi import FastAPI
from app.routes import router as main_router
from app.models import create_database

create_database()

app = FastAPI()
app.include_router(main_router)
