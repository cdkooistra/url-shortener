from fastapi import APIRouter, HTTPException, Response, Security, Header
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBearer
import os
from auth.services import verify_user, create_user, update_password
from auth.models import SessionDep, UserModel
from sqlmodel import select
from auth.schemas import UserSchema
from auth.jwt import create_jwt, verify_jwt


router = APIRouter()

# Get a list of created users
@router.get("/", status_code=200)
def list_users(session: SessionDep):
    keys = session.exec(select(UserModel.username)).all()
    if not keys:
        return JSONResponse({}, status_code=200)
    return JSONResponse(keys, status_code=200)

@router.post("/users", status_code=201)
def create_new_users(user: UserSchema, session: SessionDep):

    if not create_user(user.username, user.password, session):
        raise HTTPException(status_code=409, detail="Duplicate")
    
    return {"message": "User created successfully"}


@router.put("/users", status_code=200)
def update_user_password(username: str, old_password: str, new_password: str, session: SessionDep):

    if not update_password(username, old_password, new_password, session):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return {"message": "Password updated successfully"}

@router.post("/users/login")
def login(user: UserSchema, session: SessionDep):
    """Logs in a user and returns a JWT if credentials are valid."""
    token = verify_user(user.username, user.password, session)
    
    if not token:
        raise HTTPException(status_code=403, detail="Forbidden") 
    
    return {"token": token, "token_type": "bearer"}

# Additional get for verifying user's token on app
@router.get("/users/verify")
def verify_user_token(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=403, detail="Forbidden")

    payload = verify_jwt(authorization)  # Use raw token

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


@router.get("/debug/env/")
def debug_env(variable_name: str, response: Response):
    # WARNING: Exposing environment variables in production can be a security risk.
    return {variable_name: os.environ.get(variable_name, "Not Found")}

@router.get("/debug/jwt")
def debug_jwt():
    test_payload = {"user_id": 123, "role": "admin"}
    token = create_jwt(test_payload)
    decoded_payload = verify_jwt(token)
    return {"token": token, "decoded_payload": decoded_payload}