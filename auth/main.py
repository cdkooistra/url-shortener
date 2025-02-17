from fastapi import FastAPI
from auth.routes import router as auth_router
from auth.models import create_database
from dotenv import load_dotenv

load_dotenv()           # we should be passing secrets as env variables in a .env file
                        # look at my example.env file for reference
create_database()

app = FastAPI()
app.include_router(auth_router)
