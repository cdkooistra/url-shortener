from fastapi import FastAPI
from app.routes import router as main_router
# dotenv?

app = FastAPI()
app.include_router(main_router)
