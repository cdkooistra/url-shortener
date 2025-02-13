from fastapi import APIRouter
import os
from fastapi import Response

router = APIRouter()

# @router.post("/users")
# params: username, password
# do: create user with username and password and store in db -> user_table
# return 201, 409 if user already exists

# @router.put("/users")
# params: username, old-password, new-password
# do: update password for user with username and old-password
# return 200, 403 if old-password does not match

# @router.post("/users/login")
# params: username, password
# do: verify if user exists in table and generate a JWT token
# return 200, 403 if user does not exist

@router.get("/debug/env/")
def debug_env(variable_name: str, response: Response):
    # WARNING: Exposing environment variables in production can be a security risk.
    return {variable_name: os.environ.get(variable_name, "Not Found")}