from fastapi import APIRouter, HTTPException, Response, Depends
import os
from app.auth.auth import verify_user
from app.models import SessionDep
from sqlmodel import Session
from app.schemas import UserSchema

router = APIRouter()

# @router.post("/users")
# params: username, password
# do: create user with username and password and store in db -> user_table
# return 201, 409 if user already exists

#TODO: Work in progress, gets 500 internal error with TypeError: __init__() takes 1 positional argument but 4 were given

@router.post("/users", status_code=201)
def create_new_users(user: UserSchema, session: SessionDep):
    success = UserSchema(user.username, user.password, session)
    
    if not success:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    return {"message": "User created successfully"}

# @router.put("/users")
# params: username, old-password, new-password
# do: update password for user with username and old-password
# return 200, 403 if old-password does not match

# @router.post("/users/login")
# params: username, password
# do: verify if user exists in table and generate a JWT token
# return 200, 403 if user does not exist

@router.post("/users/login")
def login(username: str, password: str, session: SessionDep):
    """Logs in a user and returns a JWT if credentials are valid."""
    token = verify_user(username, password, session)
    
    if token is None:
        raise HTTPException(status_code=403, detail="Invalid credentials")  # Using 403 per your comment
    
    return {"access_token": token, "token_type": "bearer"}


@router.get("/debug/env/")
def debug_env(variable_name: str, response: Response):
    # WARNING: Exposing environment variables in production can be a security risk.
    return {variable_name: os.environ.get(variable_name, "Not Found")}