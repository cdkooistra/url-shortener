from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse, Response
import os
from auth.services import verify_user, create_user
from auth.models import SessionDep, UserModel
from sqlmodel import Session, select
from auth.schemas import UserSchema
from auth.jwt import create_jwt, verify_jwt
router = APIRouter()


@router.get("/", status_code=200)
def list_users(session: SessionDep):
    keys = session.exec(select(UserModel.username)).all()
    if not keys:
        return JSONResponse({}, status_code=200)
    return JSONResponse(keys, status_code=200)

# @router.post("/users")
# params: username, password
# do: create user with username and password and store in db -> user_table
# return 201, 409 if user already exists

@router.post("/users", status_code=201)
def create_new_users(user: UserSchema, session: SessionDep):

    if not create_user(user.username, user.password, session):
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

@router.get("/debug/jwt")
def debug_jwt():
    test_payload = {"user_id": 123, "role": "admin"}
    token = create_jwt(test_payload)
    decoded_payload = verify_jwt(token)
    return {"token": token, "decoded_payload": decoded_payload}