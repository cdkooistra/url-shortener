from fastapi import FastAPI
from app.routes import router as main_router
from app.auth.routes import router as auth_router
from app.models import create_database
from dotenv import load_dotenv

load_dotenv()           # we should be passing secrets as env variables in a .env file
                        # look at my example.env file for reference
create_database()

app = FastAPI()
app.include_router(main_router)
app.include_router(auth_router, prefix="/auth")
